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
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tests', views.get_tests),
    path('api/answer_question', views.answer_question),
    path('api/create_session', views.create_session),
    path('api/get_test_result/<int:accauntId>/<int:sessionId>',views.get_test_result),
    path('api/signin', views.create_accaunt),
    path('api/auth', views.login_accaunt),
    path('api/create_question', views.create_question),
    path('api/create_test', views.create_test),
    path('api/add_questions_to_test', views.add_questions_to_test),
    path('api/token/refresh/', TokenRefreshView.as_view())
]
