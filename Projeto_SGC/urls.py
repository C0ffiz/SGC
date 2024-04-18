from django.contrib import admin
from django.urls import path
from App_SGC import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register',views.register,name='register'),
    path('signin',views.verificaLogin,name='verificaLogin'),
    path('signup',views.realizaRegistro,name='realizaRegistro'),
    path('admin/', admin.site.urls),
#   path('usuarios/',views.usuarios,name='listagem_usuarios')
]

