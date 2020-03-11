"""POS_61070068 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from . import views
urlpatterns = [
    path('list/<int:manage_type>', views.manage, name='manage'),
   # path('type/', views.manage_type, name='manage_type'),
    path('edit/<int:manage_type>/<int:id>', views.edit, name='edit'),
    path('delete/<int:manage_type>/<int:id>', views.delete, name='delete'),
    path('create/<int:manage_type>', views.create, name='create'),
    
]
