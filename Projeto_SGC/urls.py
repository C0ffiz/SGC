from django.contrib import admin
from django.urls import path
from App_SGC import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.exibirLogin,name='exibirLogin'),
#    path('register',views.register,name='register'),
    path('signin',views.verificarLogin,name='verificarLogin'),
    path('signup',views.inserirUsuario,name='inserirUsuario'),
   
#   path('usuarios/',views.usuarios,name='listagem_usuarios')
]

