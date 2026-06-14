from django.contrib import admin
from django.urls import include, path
from core.views import auth_login, auth_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_login, name='login'),
    path('logout/', auth_logout, name='logout'),
    path('', include('core.urls')),
]