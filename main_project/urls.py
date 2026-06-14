from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls), # Стандартная админка Django
    path('', include('core.urls')), # Подключаем наши URL из приложения core
]