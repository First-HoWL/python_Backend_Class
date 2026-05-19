"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from library import views

handler404 = "library.views.get404"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.get_main_page, name="main"),
    path('schedule/', views.get_week_schedule, name="schedule"),
    path('today/', views.get_today_schedule, name="today"),
    path('day/<str:day>', views.get_day, name="day"),
    path('teachers/', views.get_teachers, name="teachers")
    
]
