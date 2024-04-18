from django.contrib import admin
from django.urls import path
from App_SGC import views

urlpatterns = [
    path('',views.login,name='login'),
    path('signin',views.verificaLogin,name='verificaLogin')
#   path('usuarios/',views.usuarios,name='listagem_usuarios')
]

