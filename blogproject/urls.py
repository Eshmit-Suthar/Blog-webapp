from django.contrib import admin
from django.urls import path, include
from blog import views  # ✅ Import your views file

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main blog app
    path('', include('blog.urls')),

    # 🚪 Custom logout (with success message)
    path('accounts/logout/', views.custom_logout, name='logout'),

    # Built-in Django auth system (login, password management)
    path('accounts/', include('django.contrib.auth.urls')),
]
