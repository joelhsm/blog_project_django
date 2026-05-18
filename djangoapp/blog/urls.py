from django.urls import path
# from blog.views import index, post, page, created_by, category, tag, search
from blog.views import PostListView, PostDetailView, PageDetailView, CreatedByListView, CategoryListView, TagListView, SearchListView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('created-by/<int:author_pk>/', CreatedByListView.as_view(), name='created_by'),
    path('category/<slug:category_slug>/', CategoryListView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', TagListView.as_view(), name='tag'),
    path('search/', SearchListView.as_view(), name='search'),
]