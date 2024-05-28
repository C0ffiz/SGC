#  Login
from django.contrib import admin
from django.urls import path
from App_SGC import views
from App_SGC.views import CondominosListViews,CondominosCreateViews,CondominosUpdateViews,CondominosDeleteViews
from App_SGC.views import UsuariosListViews,UsuariosCreateViews,UsuariosUpdateViews,UsuariosDeleteViews


#  Condomino
from django.views.generic import ListView
# CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',UsuariosListViews.as_view(template_name="usuarios/usuarios_list.html"), name="usuarios_list"),
    #  path('',CondominosListViews.as_view(template_name="condominos/condominos_list.html"), name="condominos_list"),

#  Caminhos do Login
    path('login',views.exibirLogin,name='exibirLogin'),
    path('signin',views.verificarLogin,name='verificarLogin'),
    # path('signup',views.inserirUsuario,name='inserirUsuario'),

    #  Caminhos da home
    path('home',views.exibirHome,name='exibirHome'),

#  Caminhos do Usuário
    # path('usuario',views.exibirLogin,name='exibirLogin'),
    # path('signin',views.verificarLogin,name='verificarLogin'),

#  Caminhos do Usuário 
    path('usuarios_list',UsuariosListViews.as_view(template_name="usuarios/usuarios_list.html"), name="usuarios_list"),
    path('usuarios_create',UsuariosCreateViews.as_view(template_name="usuarios/usuarios_create.html"), name="usuarios_create"),
    path('usuarios_update/<str:pk>', UsuariosUpdateViews.as_view(template_name="usuarios/usuarios_update.html"), name="usuarios_update"),
    path("usuarios_delete/<str:pk>", UsuariosDeleteViews.as_view(template_name="usuarios/usuarios_confirm_delete.html"), name="usuarios_delete"),

   
#  Caminhos do Condômino 
    path('condominos_list',CondominosListViews.as_view(template_name="condominos/condominos_list.html"), name="condominos_list"),
    path('condominos_create',CondominosCreateViews.as_view(template_name="condominos/condominos_create.html"), name="condominos_create"),
    path("update/<int:pk>", CondominosUpdateViews.as_view(template_name="condominos/condominos_update.html"), name="condominos_update"),
    path("delete/<int:pk>", CondominosDeleteViews.as_view(template_name="condominos/condominos_confirm_delete.html"), name="condominos_delete"),

]

