# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),  # home page — show all posts
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # single post page
    path('post/new/', views.post_new, name='post_new'),  # create new post
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),  # edit post
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),  # delete post
    path('register/', views.register, name='register'),  # user registration
]
