from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main blog app
    path('', include('blog.urls')),

    # Built-in Django auth system (login, logout, password management)
    path('accounts/', include('django.contrib.auth.urls')),
]
