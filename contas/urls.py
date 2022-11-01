from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('login/', obtain_auth_token, name='user-login'),
    path('usuario/', views.CriarContasClientView.as_view(), name='user-create-client'),
    path('funcionario/', views.CriarContasFuncionarioView.as_view(), name='user-create-employee'),    
]