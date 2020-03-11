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
from shop import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/<int:id>', views.Add_To_Cart, name='Add_To_Cart'),
    path('sale/', views.sale, name='sale'),
    path('dalete/<int:id>', views.delete, name='delete'),
    path('recal/<str:id>/<str:amount>', views.recalculate, name='recal'),
]
