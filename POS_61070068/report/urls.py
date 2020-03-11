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
    path('search/<int:day>/<int:month>/<int:year>/<int:week>', views.report_search, name='report_search'),
    path('search/<int:day>/<int:month>/<int:year>/', views.report_search_day, name='report_search_day'),
    path('search/<int:month>/<int:year>/', views.report_search_month, name='report_search_month'),
    path('search/<int:year>/', views.report_search_year, name='report_search_year'),
    path('search/<int:year>/<int:week>', views.report_search_week, name='report_search_week'),
    path('<str:report_type>/', views.report, name='report_list'),
    
]
