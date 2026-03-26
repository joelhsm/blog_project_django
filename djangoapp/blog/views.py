from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import Http404

posts = list(range(1000))


def index(request):
    posts = Post.objects.get_published()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'tab_title': 'Home'
        }
    )

def created_by(request, author_pk):
    user = User.objects.get(pk=author_pk)
    if not user:
        raise Http404("Autor não encontrado")
    
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if user.first_name:
        tab_title = f'{user.first_name} {user.last_name}'.capitalize()
    else:
        tab_title = None

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'tab_title': tab_title
        }
    )

def category(request, category_slug):
    posts = Post.objects.get_published().filter(category__slug=category_slug)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'tab_title': 'Categoria'
        }
    )

def tag(request, tag_slug):
    posts = Post.objects.get_published().filter(tags__slug=tag_slug)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'tab_title': 'Tag'
        }
    )


def search(request):
    search_term = request.GET.get('search', '').strip()

    if not search_term:
        return redirect('blog:index')

    posts = Post.objects.get_published().filter(
        Q(title__icontains=search_term) |
        Q(content__icontains=search_term) |
        Q(excerpt__icontains=search_term) |
        Q(category__name__icontains=search_term) |
        Q(tags__name__icontains=search_term) |
        Q(created_by__first_name__icontains=search_term) |
        Q(created_by__last_name__icontains=search_term)
    )

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'search_value': search_term,
            'tab_title': 'Busca'
        }
    )


def page(request, slug):
    page_obj = Page.objects.get_published().filter(slug=slug).first()
    tab_title = page_obj.slug.replace("-", " ").capitalize()
    
    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'tab_title': tab_title
        }
    )


def post(request, slug):
    post = Post.objects.get_published().filter(slug=slug).first()

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
            'tab_title': 'Post'
        }
    )