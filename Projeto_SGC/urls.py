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
from App_SGC.views import BeneficiosListViews,BeneficiosCreateViews,BeneficiosUpdateViews,BeneficiosDeleteViews
from App_SGC.views import BeneficiosRecebidosListViews,BeneficiosRecebidosCreateViews,BeneficiosRecebidosUpdateViews,BeneficiosRecebidosDeleteViews
from App_SGC.views import FinanceiroEstruturaListViews,FinanceiroEstruturaCreateViews,FinanceiroEstruturaUpdateViews,FinanceiroEstruturaDeleteViews
from App_SGC.views import ReceitaListViews,ReceitaCreateViews,ReceitaUpdateViews,ReceitaDeleteViews
from App_SGC.views import DespesasListViews,DespesasCreateViews,DespesasUpdateViews,DespesasDeleteViews
from App_SGC.views import CorrespondenciasListViews,CorrespondenciasCreateViews,CorrespondenciasUpdateViews,CorrespondenciasDeleteViews
from App_SGC.views import EspacosAdmListViews,EspacosAdmCreateViews,EspacosAdmUpdateViews,EspacosAdmDeleteViews
from App_SGC.views import TiposPatrimonioListViews,TiposPatrimonioCreateViews,TiposPatrimonioUpdateViews,TiposPatrimonioDeleteViews
from App_SGC.views import PatrimonioListViews,PatrimonioCreateViews,PatrimonioUpdateViews,PatrimonioDeleteViews
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
    path('financeiro_estrutura_list', FinanceiroEstruturaListViews.as_view(template_name="estrutura-financeiro/financeiro_list.html"), name="financeiro_estrutura_list"),
    path('financeiro_estrutura_create', FinanceiroEstruturaCreateViews.as_view(template_name="estrutura-financeiro/financeiro_create.html"), name="financeiro_estrutura_create"),
    path('financeiro_estrutura_update/<int:pk>', FinanceiroEstruturaUpdateViews.as_view(template_name="estrutura-financeiro/financeiro_update.html"), name="financeiro_estrutura_update"),
    path('financeiro_estrutura_delete/<int:pk>', FinanceiroEstruturaDeleteViews.as_view(template_name="estrutura-financeiro/financeiro_confirm_delete.html"), name="financeiro_estrutura_delete"),

#  Caminhos das Receitas
    path('receita_list', ReceitaListViews.as_view(template_name="receitas/receitas_list.html"), name="receita_list"),
    path('receita_create', ReceitaCreateViews.as_view(template_name="receitas/receitas_create.html"), name="receita_create"),
    path('receita_update/<int:pk>', ReceitaUpdateViews.as_view(template_name="receitas/receitas_update.html"), name="receita_update"),
    path('receita_delete/<int:pk>', ReceitaDeleteViews.as_view(template_name="receitas/receitas_confirm_delete.html"), name="receita_delete"),

#  Caminhos das Despesas
    path('despesas_list', DespesasListViews.as_view(template_name="despesas/despesas_list.html"), name="despesas_list"),
    path('despesas_create', DespesasCreateViews.as_view(template_name="despesas/despesas_create.html"), name="despesas_create"),
    path('despesas_update/<int:pk>', DespesasUpdateViews.as_view(template_name="despesas/despesas_update.html"), name="despesas_update"),
    path('despesas_delete/<int:pk>', DespesasDeleteViews.as_view(template_name="despesas/despesas_confirm_delete.html"), name="despesas_delete"),


#  Caminhos dos Benefícios
    path('beneficios_list', BeneficiosListViews.as_view(template_name="beneficios/beneficios_list.html"), name="beneficios_list"),
    path('beneficios_create', BeneficiosCreateViews.as_view(template_name="beneficios/beneficios_create.html"), name="beneficios_create"),
    path('beneficios_update/<int:pk>', BeneficiosUpdateViews.as_view(template_name="beneficios/beneficios_update.html"), name="beneficios_update"),
    path('beneficios_delete/<int:pk>', BeneficiosDeleteViews.as_view(template_name="beneficios/beneficios_confirm_delete.html"), name="beneficios_delete"),


#  Caminhos dos Benefícios recebidos pelos Calaboradores
    path('beneficios_recebidos_list/', BeneficiosRecebidosListViews.as_view(template_name="beneficios_recebidos/beneficios_recebidos_list.html"), name="beneficios_recebidos_list"),
    path('beneficios_recebidos_create/', BeneficiosRecebidosCreateViews.as_view(template_name="beneficios_recebidos/beneficios_recebidos_create.html"), name="beneficios_recebidos_create"),
    path('beneficios_recebidos_update/<int:pk>/', BeneficiosRecebidosUpdateViews.as_view(template_name="beneficios_recebidos/beneficios_recebidos_update.html"), name="beneficios_recebidos_update"),
    path('beneficios_recebidos_delete/<int:pk>/', BeneficiosRecebidosDeleteViews.as_view(template_name="beneficios_recebidos/beneficios_recebidos_confirm_delete.html"), name="beneficios_recebidos_delete"),


#  Caminhos de Correspondências
    path('correspondencias_list', CorrespondenciasListViews.as_view(template_name="correspondencias/correspondencias_list.html"), name="correspondencias_list"),
    path('correspondencias_create', CorrespondenciasCreateViews.as_view(template_name="correspondencias/correspondencias_create.html"), name="correspondencias_create"),
    path('correspondencias_update/<str:pk>', CorrespondenciasUpdateViews.as_view(template_name="correspondencias/correspondencias_update.html"), name="correspondencias_update"),
    path('correspondencias_delete/<str:pk>', CorrespondenciasDeleteViews.as_view(template_name="correspondencias/correspondencias_confirm_delete.html"), name="correspondencias_delete"),


#  Caminhos de Locais Administrativos
    path('espacosAdm_list', EspacosAdmListViews.as_view(template_name="espacosAdm/espacosAdm_list.html"), name="espacosAdm_list"),
    path('espacosAdm_create', EspacosAdmCreateViews.as_view(template_name="espacosAdm/espacosAdm_create.html"), name="espacosAdm_create"),
    path('espacosAdm_update/<int:pk>/', EspacosAdmUpdateViews.as_view(template_name="espacosAdm/espacosAdm_update.html"), name="espacosAdm_update"),
    path('espacosAdm_delete/<str:pk>', EspacosAdmDeleteViews.as_view(template_name="espacosAdm/espacosAdm_confirm_delete.html"), name="espacosAdm_delete"),


#  Caminhos dos Tipos de Patrimônio
    path('tiposPatrimonio_list', TiposPatrimonioListViews.as_view(template_name="tiposPatrimonio/tiposPatrimonio_list.html"), name="tiposPatrimonio_list"),
    path('tiposPatrimonio_create', TiposPatrimonioCreateViews.as_view(template_name="tiposPatrimonio/tiposPatrimonio_create.html"), name="tiposPatrimonio_create"),
    path('tiposPatrimonio_update/<str:pk>', TiposPatrimonioUpdateViews.as_view(template_name="tiposPatrimonio/tiposPatrimonio_update.html"), name="tiposPatrimonio_update"),
    path('tiposPatrimonio_delete/<str:pk>', TiposPatrimonioDeleteViews.as_view(template_name="tiposPatrimonio/tiposPatrimonio_confirm_delete.html"), name="tiposPatrimonio_delete"),


#  Caminhos do Patrimônio
    path('patrimonio_list', PatrimonioListViews.as_view(template_name="patrimonio/patrimonio_list.html"), name="patrimonio_list"),
    path('patrimonio_create', PatrimonioCreateViews.as_view(template_name="patrimonio/patrimonio_create.html"), name="patrimonio_create"),
    path('patrimonio_update/<str:pk>', PatrimonioUpdateViews.as_view(template_name="patrimonio/patrimonio_update.html"), name="patrimonio_update"),
    path('patrimonio_delete/<str:pk>', PatrimonioDeleteViews.as_view(template_name="patrimonio/patrimonio_confirm_delete.html"), name="patrimonio_delete"),









#  Caminhos SUBSISTEMA FINANCEIRO



]






