from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('custom_auth.urls')),  # Убедитесь, что нет лишних пробелов
]