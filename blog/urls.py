from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/new/', views.post_create, name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/like/', views.toggle_like, name='post_like'),
      path('post/<int:pk>/like/ajax/', views.toggle_like_ajax, name='post_like_ajax'),
      path('post/<int:pk>/comment/ajax/', views.add_comment_ajax, name='post_comment_ajax'),
      path('post/<int:pk>/publish/', views.toggle_publish, name='post_publish'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('search/', views.search_profiles, name='search_profiles'),
    path('search/posts/', views.search_posts, name='search_posts'),
    path('search/all/', views.search_all, name='search_all'),
  path('inbox/', views.inbox, name='inbox'),
  path('chat/<str:username>/', views.chat_view, name='chat'),
  path('chat/<str:username>/send/', views.send_message_ajax, name='chat_send_ajax'),
  path('chat/<str:username>/messages/ajax/', views.chat_messages_ajax, name='chat_messages_ajax'),
  path('comment/<int:pk>/like/ajax/', views.toggle_comment_like_ajax, name='comment_like_ajax'),
]