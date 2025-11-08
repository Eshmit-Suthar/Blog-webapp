from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # HOME
    path('', views.home, name='home'),
    
    # POST URLS (specific patterns FIRST)
    path('post/new/', views.post_create, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    
    # POST DETAIL (generic pattern LAST)
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
  path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),



    # PROFILE URLS (specific FIRST)
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    
    # AUTHENTICATION
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),  # ✅ Make sure this line exists
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
