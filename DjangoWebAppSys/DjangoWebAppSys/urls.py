"""DjangoWebAppSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from WebApp import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin_panel'),
    path('', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('main/', views.main_page, name='main'),
    path('register/', views.register_page, name='register'),
    path('get_main_data', views.get_main_data, name='get_main_data'),
    path('view_blacklist/', views.view_blacklist, name='view_blacklist'),
    path('view_users/', views.view_users_page, name='view_users'),
    path('user_del/<username>/', views.user_del, name='user_del'),
    path('logged_data/', views.logged_data_page, name='logged_data'),
]
