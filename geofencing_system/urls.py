"""
URL configuration for geofencing_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from geofencing import views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', views.login_view, name='login'),  # Root URL redirects to login page
    path('login/', views.login_view, name='login'),
    path('index/', views.index, name='index'), 
    path('check_geofence/', views.check_geofence, name='check_geofence'),
    path('record_action/', views.record_action, name='record_action'),
    path('logout/', views.logout_view, name='logout'),
]
