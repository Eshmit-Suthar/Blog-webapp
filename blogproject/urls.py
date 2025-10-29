# BlogWebapp/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # includes your app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # for login/logout/password reset
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
