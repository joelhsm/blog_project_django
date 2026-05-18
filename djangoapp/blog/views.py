from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post, Page, Category, Tag
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView

PER_PAGE = 5

#CBV - Class Based View
class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    # ordering = ['-pk']
    queryset = Post.objects.get_published()

    # def get_queryset(self):
    #     return Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tab_title'] = 'Home'
        return context

#FBV - Function Based View
# def index(request):
#     posts = Post.objects.get_published()
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'tab_title': 'Home'
#         }
#     )

#CBV - Class Based View
class CreatedByListView(PostListView):
    def get_queryset(self):
        return Post.objects.get_published().filter(created_by__pk=self.kwargs['author_pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.filter(pk=self.kwargs['author_pk']).first()
        if user:
            if user.first_name:
                context['tab_title'] = f'{user.first_name} {user.last_name}'
            else:
                context['tab_title'] = None
        else:
            context['tab_title'] = 'Autor não encontrado'
        return context
    
#FBV - Function Based View
# def created_by(request, author_pk):
#     user = User.objects.filter(pk=author_pk).first()

#     if user:
#         posts = Post.objects.get_published().filter(created_by__pk=author_pk)
#         if user.first_name:
#             tab_title = f'{user.first_name} {user.last_name}'.capitalize()
#         else:
#             tab_title = None
#     else:
#         posts = Post.objects.none()
#         tab_title = 'Autor não encontrado'
    
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

    

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'tab_title': tab_title
#         }
#     )

#CBV - Class Based View
class CategoryListView(PostListView):
    def get_queryset(self):
        posts = Post.objects.get_published().filter(category__slug=self.kwargs['category_slug'])
        if posts:
            return posts
        else:
            return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.filter(slug=self.kwargs['category_slug']).first()
        if category:
            context['tab_title'] = category.name
        else:
            context['tab_title'] = 'Categoria não encontrada'
        return context
    
#FBV - Function Based View
# def category(request, category_slug):
#     posts = Post.objects.get_published().filter(category__slug=category_slug)
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'tab_title': 'Categoria'
#         }
#     )

#CBV - Class Based View
class TagListView(PostListView):
    def get_queryset(self):
        posts = Post.objects.get_published().filter(tags__slug=self.kwargs['tag_slug'])
        if posts:
            return posts
        else:
            return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.filter(slug=self.kwargs['tag_slug']).first()
        if tag:
            context['tab_title'] = tag.name
        else:
            context['tab_title'] = 'Tag não encontrada'
        return context

#FBV - Function Based View
# def tag(request, tag_slug):
#     posts = Post.objects.get_published().filter(tags__slug=tag_slug)
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'tab_title': 'Tag'
#         }
#     )


#CBV - Class Based View
class SearchListView(PostListView):
    def get_queryset(self):
        search_term = self.request.GET.get('search', '').strip()
        if not search_term:
            return Post.objects.none()
        return Post.objects.get_published().filter(
            Q(title__icontains=search_term) |
            Q(content__icontains=search_term) |
            Q(excerpt__icontains=search_term) |
            Q(category__name__icontains=search_term) |
            Q(tags__name__icontains=search_term) |
            Q(created_by__first_name__icontains=search_term) |
            Q(created_by__last_name__icontains=search_term)
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('search', '').strip()
        context['search_value'] = search_term
        context['tab_title'] = search_term.capitalize()
        return context

#FBV - Function Based View
# def search(request):
#     search_term = request.GET.get('search', '').strip()

#     if not search_term:
#         return redirect('blog:index')

#     posts = Post.objects.get_published().filter(
#         Q(title__icontains=search_term) |
#         Q(content__icontains=search_term) |
#         Q(excerpt__icontains=search_term) |
#         Q(category__name__icontains=search_term) |
#         Q(tags__name__icontains=search_term) |
#         Q(created_by__first_name__icontains=search_term) |
#         Q(created_by__last_name__icontains=search_term)
#     )

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'search_value': search_term,
#             'tab_title': 'Busca'
#         }
#     )

#CBV - Class Based View
class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['tab_title'] = self.object.title
        else:
            context['tab_title'] = 'Página não encontrada'
        return context
    
    def get_queryset(self):
        return Page.objects.get_published()

    def get_object(self, queryset=None):
        try:
            # Tenta executar o comportamento padrão
            return super().get_object(queryset)
        except Http404:
            # Se não encontrar, retorna None em vez de dar erro 404
            return None
    

#FBV - Function Based View
# def page(request, slug):
#     page_obj = Page.objects.get_published().filter(slug=slug).first()

#     if page_obj:
#         tab_title = page_obj.title
#     else:
#         tab_title = 'Página não encontrada'
    
#     return render(
#         request,
#         'blog/pages/page.html',
#         {
#             'page': page_obj,
#             'tab_title': tab_title
#         }
#     )

#CBV - Class Based View
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['tab_title'] = self.object.slug.replace("-", " ").capitalize()
        else:
            context['tab_title'] = 'Post não encontrado'
        return context
    
    def get_queryset(self):
        return Post.objects.get_published().filter(slug=self.kwargs['slug'])

    def get_object(self, queryset=None):
        try:
            # Tenta executar o comportamento padrão
            return super().get_object(queryset)
        except Http404:
            # Se não encontrar, retorna None em vez de dar erro 404
            return None
        
    
    
    

#FBV - Function Based View
def post(request, slug):
    post_obj = Post.objects.get_published().filter(slug=slug).first()

    if post_obj:
        tab_title = post_obj.slug.replace("-", " ").capitalize()
    else:
        tab_title = 'Post não encontrado'
    
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'tab_title': tab_title
        }
    )