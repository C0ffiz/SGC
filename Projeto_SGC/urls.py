#  Login
from django.contrib import admin
from django.urls import path
from App_SGC import views
from App_SGC.views import CondominosListViews,CondominosCreateViews,CondominosUpdateViews,CondominosDeleteViews
from App_SGC.views import UsuariosListViews,UsuariosCreateViews,UsuariosUpdateViews,UsuariosDeleteViews
from App_SGC.views import CondominiosListViews,CondominiosCreateViews,CondominiosUpdateViews,CondominiosDeleteViews
from App_SGC.views import MoradoresListViews,MoradoresCreateViews,MoradoresUpdateViews,MoradoresDeleteViews
from App_SGC.views import BlocosListViews,BlocosCreateViews,BlocosUpdateViews,BlocosDeleteViews
from App_SGC.views import UnidadesListViews,UnidadesCreateViews,UnidadesUpdateViews,UnidadesDeleteViews
from App_SGC.views import VeiculosListViews,VeiculosCreateViews,VeiculosUpdateViews,VeiculosDeleteViews
from App_SGC.views import ColaboradoresListViews,ColaboradoresCreateViews,ColaboradoresUpdateViews,ColaboradoresDeleteViews
from App_SGC.views import GaragensListViews,GaragensCreateViews,GaragensUpdateViews,GaragensDeleteViews
from App_SGC.views import MudancasListViews,MudancasCreateViews,MudancasUpdateViews,MudancasDeleteViews
from App_SGC.views import OcorrenciasListViews,OcorrenciasCreateViews,OcorrenciasUpdateViews,OcorrenciasDeleteViews
from App_SGC.views import EstruturaPcListViews,EstruturaPcCreateViews,EstruturaPcUpdateViews,EstruturaPcDeleteViews
from django.views.generic import ListView
from django.urls import reverse_lazy



urlpatterns = [

#  Caminho do Admin
    path('admin/', admin.site.urls),



#  Caminhos do Login    
    path('',views.exibirLogin,name='exibirLogin'), 
    path('login',views.exibirLogin,name='exibirLogin'),
    path('signin',views.verificarLogin,name='verificarLogin'),
    
 
#  Caminhos da home
    path('home',views.exibirHome,name='exibirHome'),


#  Caminhos do Usuário 
    path('usuarios_list',UsuariosListViews.as_view(template_name="usuarios/usuarios_list.html"), name="usuarios_list"),
    path('usuarios_create',UsuariosCreateViews.as_view(template_name="usuarios/usuarios_create.html"), name="usuarios_create"),
    path('usuarios_update/<str:pk>',UsuariosUpdateViews.as_view(template_name="usuarios/usuarios_update.html"), name="usuarios_update"),
    path("usuarios_delete/<str:pk>",UsuariosDeleteViews.as_view(template_name="usuarios/usuarios_confirm_delete.html"), name="usuarios_delete"),

   
#  Caminhos do Condômino 
    path('condominos_list',CondominosListViews.as_view(template_name="condominos/condominos_list.html"), name="condominos_list"),
    path('condominos_create',CondominosCreateViews.as_view(template_name="condominos/condominos_create.html"), name="condominos_create"),
    path("update/<int:pk>", CondominosUpdateViews.as_view(template_name="condominos/condominos_update.html"), name="condominos_update"),
    path("delete/<int:pk>", CondominosDeleteViews.as_view(template_name="condominos/condominos_confirm_delete.html"), name="condominos_delete"),


#  Caminhos do Condominio
    path('condominios_list',CondominiosListViews.as_view(template_name="condominios/condominios_list.html"), name="condominios_list"),
    path('condominios_create',CondominiosCreateViews.as_view(template_name="condominios/condominios_create.html"), name="condominios_create"),
    path('condominios_update/<str:pk>',CondominiosUpdateViews.as_view(template_name="condominios/condominios_update.html"), name="condominios_update"),
    path("condominios_delete/<str:pk>",CondominiosDeleteViews.as_view(template_name="condominios/condominios_confirm_delete.html"), name="condominios_delete"),

#  Caminhos do Morador 
    path('moradores_list',MoradoresListViews.as_view(template_name="moradores/moradores_list.html"), name="moradores_list"),
    path('moradores_verify',views.verificar_cpf_condomino,name='verificar_cpf_condomino'),
    path('moradores_create/',MoradoresCreateViews.as_view(template_name="moradores/moradores_create.html"), name="moradores_create"),
    path('moradores_update/<str:pk>/', MoradoresUpdateViews.as_view(), name="moradores_update"),
    path("moradores_delete/<str:pk>",MoradoresDeleteViews.as_view(template_name="moradores/moradores_confirm_delete.html"), name="moradores_delete"),
    path('verificar_cpf_condomino/', views.verificar_cpf_condomino, name='verificar_cpf_condomino'),

#  Caminhos do Bloco 
    path('blocos_list',BlocosListViews.as_view(template_name="blocos/blocos_list.html"), name="blocos_list"),
    path('blocos_create',BlocosCreateViews.as_view(template_name="blocos/blocos_create.html"), name="blocos_create"),
    path('blocos_update/<str:pk>',BlocosUpdateViews.as_view(template_name="blocos/blocos_update.html"), name="blocos_update"),
    path("blocos_delete/<str:pk>",BlocosDeleteViews.as_view(template_name="blocos/blocos_confirm_delete.html"), name="blocos_delete"),

#  Caminhos das Unidades
    path('unidades_list',UnidadesListViews.as_view(template_name="unidades/unidades_list.html"), name="unidades_list"),
    path('unidades_create',UnidadesCreateViews.as_view(template_name="unidades/unidades_create.html"), name="unidades_create"),
    path('unidades_update/<str:pk>',UnidadesUpdateViews.as_view(template_name="unidades/unidades_update.html"), name="unidades_update"),
    path("unidades_delete/<str:pk>",UnidadesDeleteViews.as_view(template_name="unidades/unidades_confirm_delete.html"), name="unidades_delete"),

#  Caminhos de Veículos
    path('veiculos_list',VeiculosListViews.as_view(template_name="veiculos/veiculos_list.html"), name="veiculos_list"),
    path('veiculos_create',VeiculosCreateViews.as_view(template_name="veiculos/veiculos_create.html"), name="veiculos_create"),
    path('veiculos_update/<str:pk>',VeiculosUpdateViews.as_view(template_name="veiculos/veiculos_update.html"), name="veiculos_update"),
    path("veiculos_delete/<str:pk>",VeiculosDeleteViews.as_view(template_name="veiculos/veiculos_confirm_delete.html"), name="veiculos_delete"),


#  Caminhos dos Colaboradores
    path('colaboradores_list',ColaboradoresListViews.as_view(template_name="colaboradores/colaboradores_list.html"), name="colaboradores_list"),
    path('colaboradores_create',ColaboradoresCreateViews.as_view(template_name="colaboradores/colaboradores_create.html"), name="colaboradores_create"),
    path('colaboradores_update/<str:pk>',ColaboradoresUpdateViews.as_view(template_name="colaboradores/colaboradores_update.html"), name="colaboradores_update"),
    path("colaboradores_delete/<str:pk>",ColaboradoresDeleteViews.as_view(template_name="colaboradores/colaboradores_confirm_delete.html"), name="colaboradores_delete"),


#  Caminhos das Garagens
    path('garagens_list',GaragensListViews.as_view(template_name="garagens/garagens_list.html"), name="garagens_list"),
    path('garagens_create',GaragensCreateViews.as_view(template_name="garagens/garagens_create.html"), name="garagens_create"),
    path('garagens_update/<str:pk>',GaragensUpdateViews.as_view(template_name="garagens/garagens_update.html"), name="garagens_update"),
    path("garagens_delete/<str:pk>",GaragensDeleteViews.as_view(template_name="garagens/garagens_confirm_delete.html"), name="garagens_delete"),


#  Caminhos das Mudanças
    path('mudancas_list', MudancasListViews.as_view(template_name="mudancas/mudancas_list.html"), name="mudancas_list"),
    path('mudancas_create', MudancasCreateViews.as_view(template_name="mudancas/mudancas_create.html"), name="mudancas_create"),
    path('mudancas_update/<str:pk>', MudancasUpdateViews.as_view(template_name="mudancas/mudancas_update.html"), name="mudancas_update"),
    path('mudancas_delete/<str:pk>', MudancasDeleteViews.as_view(template_name="mudancas/mudancas_confirm_delete.html"), name="mudancas_delete"),


#  Caminhos das Ocorrências
    path('ocorrencias_list', OcorrenciasListViews.as_view(template_name="ocorrencias/ocorrencias_list.html"), name="ocorrencias_list"),
    path('ocorrencias_create', OcorrenciasCreateViews.as_view(template_name="ocorrencias/ocorrencias_create.html"), name="ocorrencias_create"),
    path('ocorrencias_update/<int:pk>', OcorrenciasUpdateViews.as_view(template_name="ocorrencias/ocorrencias_update.html"), name="ocorrencias_update"),
    path('ocorrencias_delete/<int:pk>', OcorrenciasDeleteViews.as_view(template_name="ocorrencias/ocorrencias_confirm_delete.html"), name="ocorrencias_delete"),

#  Caminhos do Plano de contas
    path('plano_conta_list', EstruturaPcListViews.as_view(template_name="estrutura-contas/plano_conta_list.html"), name="plano_conta_list"),
    path('plano_conta_create', EstruturaPcCreateViews.as_view(template_name="estrutura-contas/plano_conta_create.html"), name="plano_conta_create"),
    path('plano_conta_update/<int:pk>', EstruturaPcUpdateViews.as_view(template_name="estrutura-contas/plano_conta_update.html"), name="plano_conta_update"),
    path('plano_conta_delete/<int:pk>', EstruturaPcDeleteViews.as_view(template_name="estrutura-contas/plano_conta_confirm_delete.html"), name="plano_conta_delete"),




]






