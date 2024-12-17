"""
URL configuration for destination project.

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
from tours import views

app_name = "tours"

urlpatterns = [
    path('', views.place, name="place"),
    path('attracts/<int:p>', views.attracts, name="attracts"),
    path('details/<int:p>', views.details, name="details"),
    path('stay/<int:p>', views.stay, name="stay"),
    path('accommodation_detail/<int:p>',views.accommodation_detail,name="accommodation_detail"),
    path('adddestiny',views.add_destiny,name="adddestiny"),
    path('addaccommodate',views.add_accommodate,name="addaccommodate"),



]
