from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('blog', views.create, name='create_blog'),
    path('<int:blog_id>', views.detail, name='detail'),
    path('<int:blog_id>/upvote', views.upvote, name='upvote'),
    path('<int:blog_id>/delete', views.delete, name='delete'),
    path('search', views.search, name='search')
]