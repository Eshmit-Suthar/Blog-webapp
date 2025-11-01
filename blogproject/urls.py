from django.contrib import admin
from django.urls import path, include
from blog import views  # ✅ import custom views from your blog app

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main blog app
    path('', include('blog.urls')),

    # Built-in Django auth system (login, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Custom logout with success message
    path('accounts/logout/', views.custom_logout, name='logout'),
]
