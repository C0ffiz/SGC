# Model Sistema SGC 
from .models import CustomUser, CustomCondominio, CustomCondomino, CustomMorador, CustomBloco, CustomUnidade    
from .models import CustomVeiculo, CustomColaborador, CustomGaragem, CustomMudanca, CustomOcorrencia, CustomBeneficio
from .models import CustomBeneficioRecebido, CustomCorrespondencia, CustomEspaco, CustomReserva, CustomPets


# Models Subsistema Patrimônio
from .models import CustomPatrimonio, CustomEspacoAdm, CustomTipoPatrimonio


# Models Subsistema Financeiro
from .models import FinanceiroEstrutura, Banco, Caixa, ContaReceber, ContaPagar, SaldoCaixaBanco, PrevisaoDespesas, PrevisaoReceitas
from .models import PrevisaoDespesas, PrevisaoReceitas, Fornecedor


# Models Subsistema Produtividade
from .models import Produtividade


# Models Subsistema Metas
from .models import Meta


# Models Subsistema Enquete
from .models import Pergunta, PossivelResposta, Resposta
from django.forms import modelformset_factory





from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from django import forms
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.views import View
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
import locale
from django.db.utils import ProgrammingError
from datetime import datetime, date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import re
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.db.models import Q
from decimal import Decimal, InvalidOperation
import sys
from datetime import datetime
from django.db import transaction
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.db.models import F, Q
from django.views.decorators.csrf import csrf_exempt
import json


#-----------------------Views Login.................................................................

# Exibe Login
def exibirLogin(request):
    return render(request,'login/login.html')



# Processo de Login e Ir para Home
def verificarLogin(request):

    if request.method == 'POST':
        usuario = request.POST.get('usuario')  # Use get() to handle missing keys gracefully
        senha = request.POST.get('senha')
     
        # Check if both username and password are provided
        if usuario and senha:
            user = authenticate(username=usuario, password=senha)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'exibirHome')  # Redirect to next or home
                return redirect(next_url)
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Por favor, forneça usuário e senha válidos.')

    # If not a POST request or authentication fails, render the login page again
    return render(request, 'login/login.html')            



# Exibe Home
@login_required
def exibirHome(request):
   
    # Render home page with user-specific data here
    return render(request, 'login/home.html')



#-----------------------Views Usuário.................................................................

# Tela Lista Usuarios
class UsuariosListViews(ListView):
    model = CustomUser
    context_object_name = 'usuarios_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context



# Tela Cadastro de Usuarios
class UsuariosCreateViews(CreateView):
    model = CustomUser
    template_name = 'usuarios_create.html'
    fields = ["username", "password", "cpf_usuario", "n_condominio"]
    success_url = reverse_lazy("usuarios_list")
    widgets = {
        'n_condominio': forms.Select(attrs={'class': 'form-control'}),
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['messages'] = messages.get_messages(self.request) 

        return context      
    
    def form_valid(self, form):
        # Strip mask from CPF
        cpf_usuario = form.cleaned_data['cpf_usuario'].replace(".", "").replace("-", "")
        form.instance.cpf_usuario = cpf_usuario

        # Get the selected condominium instance
        condominio_instance = form.cleaned_data['n_condominio']

        # Assign the primary key of the selected condominium to the field
        form.instance.n_condominio_id = condominio_instance.n_condominio

        # Check if the selected condominium number exists
        if not CustomCondominio.objects.filter(n_condominio=form.instance.n_condominio_id).exists():
            messages.error(self.request, 'Número de condomínio inválido.')
            return self.form_invalid(form)
        
        # Verifica se o nome de usuário já existe
        username = form.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            messages.error(self.request, 'Nome de usuário já existe. Escolha outro nome.')
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Customize error message for existing username
        if 'username' in form.errors:
            messages.error(self.request, 'Nome de usuário já existe. Escolha outro nome..')
        return super().form_invalid(form)
    



# Tela Alteração De Usuarios
class UsuariosUpdateViews(UpdateView):
    model = CustomUser
    context_object_name = 'usuarios_list'
    fields = ["username", "password", "cpf_usuario", "n_condominio"]
    success_url = reverse_lazy("usuarios_list") 
    widgets = {
        'n_condominio': forms.Select(attrs={'class': 'form-control'}),
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['messages'] = messages.get_messages(self.request) 

        return context
    
    def form_valid(self, form):
        # Strip mask from CPF
        cpf_usuario = form.cleaned_data['cpf_usuario'].replace(".", "").replace("-", "")
        form.instance.cpf_usuario = cpf_usuario
        
        # Get the selected condominium instance
        condominio_instance = form.cleaned_data['n_condominio']

        # Assign the primary key of the selected condominium to the field
        form.instance.n_condominio_id = condominio_instance.n_condominio

        # Check if the selected condominium number exists
        if not CustomCondominio.objects.filter(n_condominio=form.instance.n_condominio_id).exists():
            messages.error(self.request, 'Número de condomínio inválido.')
            return self.form_invalid(form)
        
        return super().form_valid(form)
    



# Tela Exclusão De Usuarios
class UsuariosDeleteViews(DeleteView):
    model = CustomUser
    success_url = reverse_lazy("usuarios_list")
    



#-----------------------Views Condômino.................................................................

# Tela Lista Condominos
class CondominosListViews(LoginRequiredMixin, ListView):
    model = CustomCondomino
    context_object_name = 'condominos_list'

    def get_queryset(self):
        # Filtra os condôminos pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        return CustomCondomino.objects.filter(n_condominio=user_condominio)



# Tela Cadastro de Condôminos
@method_decorator(login_required, name='dispatch')
class CondominosCreateViews(CreateView):
    model = CustomCondomino
    fields = ["cpf_condomino", "nome_condomino", "telefone_condomino", "celular_condomino", "email_condomino", "data_aquisicao_imovel", "data_nascimento_condomino"]
    success_url = reverse_lazy("condominos_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Remove máscaras dos campos
        cpf_condomino = str(form.cleaned_data['cpf_condomino']).replace(".", "").replace("-", "")
        celular_condomino = str(form.cleaned_data['celular_condomino']).replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        
        form.instance.cpf_condomino = cpf_condomino
        form.instance.celular_condomino = celular_condomino

        # Obtém o n_condominio do usuário logado
        form.instance.n_condominio = self.request.user.n_condominio

        # Verifica se o condômino já está cadastrado
        if CustomCondomino.objects.filter(cpf_condomino=cpf_condomino, n_condominio=form.instance.n_condominio).exists():
            messages.error(self.request, 'Condômino já cadastrado')
            return self.form_invalid(form)   

        return super().form_valid(form)

    def form_invalid(self, form):
        # Customize error message
        if 'cpf_condomino' in form.errors:
            form.errors['cpf_condomino'] = ['Erro ao cadastrar o condômino']
        return super().form_invalid(form)



# Tela Alteração De Condôminos
class CondominosUpdateViews(UpdateView):
    model = CustomCondomino
    context_object_name = 'condominos_list'    
    fields = [
        "cpf_condomino", "nome_condomino", "data_nascimento_condomino", 
        "telefone_condomino", "celular_condomino", "email_condomino", 
        "data_aquisicao_imovel", "n_condominio"
    ]
    template_name = "condominos/condominos_update.html"
    success_url = reverse_lazy("condominos_list")  # Redirecionar para lista após sucesso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        # Carregar o objeto antes de modificar
        self.object = self.get_object()

        # Remover caracteres especiais de CPF e telefone
        cpf_condomino = request.POST.get('cpf_condomino', '').replace('.', '').replace('-', '')
        nome_condomino = request.POST.get('nome_condomino', '')
        data_nascimento_condomino = request.POST.get('data_nascimento_condomino', '')
        telefone_condomino = request.POST.get('telefone_condomino', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        celular_condomino = request.POST.get('celular_condomino', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        email_condomino = request.POST.get('email_condomino', '')
        data_aquisicao_imovel = request.POST.get('data_aquisicao_imovel', '')

        # Atualizar os campos da instância
        self.object.cpf_condomino = cpf_condomino
        self.object.nome_condomino = nome_condomino
        self.object.data_nascimento_condomino = data_nascimento_condomino
        self.object.telefone_condomino = telefone_condomino
        self.object.celular_condomino = celular_condomino
        self.object.email_condomino = email_condomino
        self.object.data_aquisicao_imovel = data_aquisicao_imovel

        # Obtém o n_condominio do usuário logado
        self.object.n_condominio = self.request.user.n_condominio

        try:
            self.object.save()  # Salva a instância específica
        except IntegrityError:
            messages.error(request, 'Erro ao atualizar o condômino.')
            return render(request, self.template_name, {'condominos_list': self.object})

        # Redirecionar para a URL de sucesso
        return HttpResponseRedirect(self.get_success_url())
    



# Tela Exclusão De Condôminos
class CondominosDeleteViews(DeleteView):
    model = CustomCondomino
    success_url = reverse_lazy("condominos_list")



#-----------------------Views Condôminos.................................................................

# Tela Lista Condomínios
class CondominiosListViews(ListView):
    model = CustomCondominio
    context_object_name = 'condominios_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_condominio = self.request.user.n_condominio
        context['condominios'] = CustomCondominio.objects.all
        return context



# Tela Cadastro De Condomínios
class CondominiosCreateViews(CreateView):
    model = CustomCondominio
    template_name = 'condominios_create.html'
    fields = ["n_condominio", "nome_condominio"]
    success_url = reverse_lazy("condominios_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['messages'] = messages.get_messages(self.request) 
        return context    
    
    def form_valid(self, form):
        nome_condominio = form.cleaned_data.get('nome_condominio')
        if CustomCondominio.objects.filter(nome_condominio=nome_condominio).exists():
            form.add_error('nome_condominio', 'Condomínio já cadastrado.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        # Passa os erros para o contexto do template
        return self.render_to_response(self.get_context_data(form=form))
    



# Tela Alteração De Condomínios
class CondominiosUpdateViews(UpdateView):
    model = CustomCondominio
    context_object_name = 'condominios_list'
    fields = ["n_condominio", "nome_condominio"]
    success_url = reverse_lazy("condominios_list") 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['messages'] = messages.get_messages(self.request) 
        return context      



# Tela Exclusão De Condomínios
class CondominiosDeleteViews(DeleteView):
    model = CustomCondominio
    success_url = reverse_lazy("condominios_list")
    



#-----------------------Views Moradores.................................................................

# Tela Lista Moradores
class MoradoresListViews(LoginRequiredMixin, ListView):
    model = CustomMorador
    context_object_name = 'moradores_list'
    
    def get_queryset(self):
        # Get the user's associated condominium
        user_condominio = self.request.user.n_condominio
        # Filter the residents based on the user's condominium
        return CustomMorador.objects.filter(n_condominio=user_condominio)
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os moradores pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['moradores_list'] = CustomMorador.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Verifica existência do Condômino para cadastrar moradores
@login_required  
def verificar_cpf_condomino(request):
    if request.method == 'POST':
        cpf_condomino = request.POST.get('cpf_condomino')
        cpf_condomino = cpf_condomino.replace(".", "").replace("-", "")  # Remove máscara
        user_condominio_instance = request.user.n_condominio
        
        if CustomCondomino.objects.filter(cpf_condomino=cpf_condomino, n_condominio=user_condominio_instance).exists():
            # CPF encontrado no condomínio e redireciona para a criação de moradores
            return redirect(reverse('moradores_create') + f'?cpf_condomino={cpf_condomino}')
        else:
            # Condômino não encontrado para cadastro de moradores
            messages.error(request, 'Condômino não cadastrado')
            return render(request, 'moradores/moradores_verify.html')

    return render(request, 'moradores/moradores_verify.html')



# Tela Cadastro De Moradores
@method_decorator(login_required, name='dispatch')
class MoradoresCreateViews(CreateView):
    model = CustomMorador
    template_name = 'moradores_create.html'
    fields = ["cpf_morador", "nome_morador", "data_nascimento_morador", "celular_morador",
              "email_morador", "parentesco_condomino"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cpf_condomino'] = self.request.GET.get('cpf_condomino', '')
        context['messages'] = messages.get_messages(self.request)  # Adicione esta linha p aparecer a mensagem

        return context

    def form_valid(self, form):
        # Extract the cpf_condomino value from the URL parameters
        cpf_condomino_str = self.request.GET.get('cpf_condomino', None)
        print('Entrei no form_valid ............................................')
        if cpf_condomino_str:
            # Clean up the cpf_condomino string (remove periods and dashes)
            cpf_condomino_str = cpf_condomino_str.replace(".", "").replace("-", "")

            # Find the corresponding CustomCondomino object
            condomino = CustomCondomino.objects.filter(cpf_condomino=cpf_condomino_str).first()

            if not condomino:
                messages.error(self.request, 'CPF de condômino não encontrado.')
                return self.form_invalid(form)

            # Assign the condômino and condomínio to the morador
            form.instance.cpf_condomino = condomino
            form.instance.n_condominio = condomino.n_condominio
            messages.error(self.request, 'Entre com informações de um novo morador.')

        else:
            messages.error(self.request, 'CPF do condômino não fornecido.')
            return self.form_invalid(form)

        # Remove máscara do CPF do morador
        cpf_morador = form.cleaned_data['cpf_morador'].replace(".", "").replace("-", "")
        form.instance.cpf_morador = cpf_morador

        # Verifica se o CPF do morador já está cadastrado para este condômino e condomínio
        if CustomMorador.objects.filter(cpf_morador=cpf_morador, cpf_condomino=condomino,
                                        n_condominio=condomino.n_condominio).exists():
            messages.error(self.request, 'Morador já cadastrado para este condômino e condomínio.')
            return self.form_invalid(form)

        self.object = form.save()

        # Recarrega página com o mesmo cpf
        return redirect(reverse('moradores_create') + f'?cpf_condomino={condomino.cpf_condomino}')

    def form_invalid(self, form):
        return super().form_invalid(form)    



# Tela Alteração De Moradores
class MoradoresUpdateViews(UpdateView):
    model = CustomMorador
    template_name = 'moradores/moradores_update.html'
    context_object_name = 'morador'
    fields = ["cpf_morador", "nome_morador", "data_nascimento_morador", "celular_morador", "email_morador", "parentesco_condomino"]
    success_url = reverse_lazy("moradores_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa o cpf_condomino para o contexto para renderizar no template
        context['cpf_condomino'] = self.request.GET.get('cpf_condomino', '')
        context['messages'] = messages.get_messages(self.request)
        cpf_condomino_url = self.request.GET.get('cpf_condomino', '')
        print(f'cpf_condomino na URL: {cpf_condomino_url}')
        return context    

    def form_valid(self, form):
        # Obtém o cpf_condomino do formulário
        cpf_condomino_str = self.request.POST.get('cpf_condomino', None) 
        print(f'cpf_condomino_str: {cpf_condomino_str}')  

        if cpf_condomino_str:
            # Remove máscara do CPF e busca o condômino
            cpf_condomino_str = cpf_condomino_str.replace(".", "").replace("-", "")
            condomino = CustomCondomino.objects.filter(cpf_condomino=cpf_condomino_str).first()
            if not condomino:
                messages.error(self.request, 'CPF de condômino não encontrado.')
                return self.form_invalid(form)

            form.instance.cpf_condomino = condomino
            form.instance.n_condominio = condomino.n_condominio
        else:
            messages.error(self.request, 'CPF do condômino não fornecido.')
            return self.form_invalid(form)

        # Limpa o CPF do morador e verifica duplicidade
        cpf_morador = form.cleaned_data['cpf_morador'].replace(".", "").replace("-", "")
        form.instance.cpf_morador = cpf_morador

        # Verifica duplicidade ignorando o morador atual
        if CustomMorador.objects.filter(cpf_morador=cpf_morador, cpf_condomino=condomino, n_condominio=condomino.n_condominio).exclude(pk=self.object.pk).exists():
            messages.error(self.request, 'Morador já cadastrado para este condômino e condomínio.')
            return self.form_invalid(form)

        self.object = form.save()

        # Redireciona com o pk do morador atualizado
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao cadastrar o morador.')
        print(f'Formulário inválido. Erros: {form.errors}')  # Print erros do formulário
        return super().form_invalid(form)



# Tela Exclusão De Moradores
class MoradoresDeleteViews(DeleteView):
    model = CustomMorador
    template_name = 'moradores/moradores_confirm_delete.html'
    success_url = reverse_lazy('moradores_list')



#-----------------------Views Blocos.................................................................

# Tela Lista os Blocos
class BlocosListViews(LoginRequiredMixin, ListView):
    model = CustomBloco
    context_object_name = 'blocos_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os blocos pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['blocos_list'] = CustomBloco.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro de Blocos 
@method_decorator(login_required, name='dispatch')
class BlocosCreateViews(CreateView):
    model = CustomBloco
    template_name = 'blocos_create.html'
    fields = ["bloco"]  
    success_url = reverse_lazy("blocos_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Atribuir automaticamente o n_condominio do usuário logado
        form.instance.n_condominio = self.request.user.n_condominio

        bloco_instance = form.cleaned_data['bloco']
        form.instance.bloco = bloco_instance

        # Verificar se a combinação bloco-condomínio já existe para o n_condominio do usuário
        if CustomBloco.objects.filter(bloco=form.instance.bloco, n_condominio=form.instance.n_condominio).exists():
            form.add_error(None, 'Bloco já cadastrado para este condomínio.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        form.add_error(None, 'Erro ao cadastrar o Bloco.')
        return self.render_to_response(context)



# Tela Alteração de Blocos 
class BlocosUpdateViews(UpdateView):
    model = CustomBloco
    template_name = 'blocos_update.html'
    context_object_name = 'blocos_list'
    fields = ["bloco"]
    success_url = reverse_lazy("blocos_list") 
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def form_valid(self, form):
        bloco_instance = form.cleaned_data['bloco']
        form.instance.bloco = bloco_instance

        # Verificar se a combinação bloco-condomínio já existe
        if CustomBloco.objects.filter(bloco=form.instance.bloco).exists():
            form.add_error('bloco', 'Bloco já cadastrado para este condomínio.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):        
        context = self.get_context_data(form=form)
        form.add_error(None, 'Erro ao alterar o Bloco.')
        return super().form_invalid(form)
    

       
# Tela Exclusão de Blocos
class BlocosDeleteViews(DeleteView):
    model = CustomBloco
    success_url = reverse_lazy("blocos_list")
   


  #-----------------------Views Unidades.................................................................




#-----------------------Views Unidades .................................................................

# Tela Lista as Unidades 
class UnidadesListViews(LoginRequiredMixin, ListView):
    model = CustomUnidade
    context_object_name = 'unidades_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar as unidades pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['unidades_list'] = CustomUnidade.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro de Unidades
@method_decorator(login_required, name='dispatch')
class UnidadesCreateViews(View):
    template_name = 'unidades/unidades_create.html'
    success_url = reverse_lazy("unidades_list")

    def get_context_data(self, **kwargs):
        context = {}
        user_condominio = self.request.user.n_condominio
        context['blocos'] = CustomBloco.objects.filter(n_condominio=user_condominio)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):  # Corrigido: dentro da classe
        cpf_condomino = request.POST.get('cpf_condomino')
        bloco_id = request.POST.get('bloco_id')
        unidade = request.POST.get('unidade')

        context = self.get_context_data()

        # Validar CPF do condômino
        cpf_condomino_instance = CustomCondomino.objects.filter(cpf_condomino=cpf_condomino)
        
        if not cpf_condomino_instance.exists():
            messages.error(self.request, 'Condômino não cadastrado.')
            return render(request, self.template_name, context)
     
        # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        # Validar se a unidade já existe para o bloco
        if CustomUnidade.objects.filter(bloco_id=bloco_id, unidade=unidade, n_condominio=user_condominio_instance).exists():
            messages.error(self.request, 'Unidade já cadastrada para este bloco.')
            return render(request, self.template_name, context)

        # Criar linha na tabela unidade com o n_condominio do usuário logado
        try:
            if cpf_condomino_instance and user_condominio_instance:
                CustomUnidade.objects.create(
                    cpf_condomino=cpf_condomino_instance.first(),  # Adiciona '.first()' para pegar o condômino
                    bloco_id=CustomBloco.objects.get(bloco_id=bloco_id),
                    unidade=unidade,
                    n_condominio=user_condominio_instance
                )
        except IntegrityError:
            context['form_errors'] = 'Erro ao cadastrar'
            return render(request, self.template_name, context)
        
        except Exception as e:
            context['form_errors'] = f'Ocorreu erro inesperado: {str(e)}'
            return render(request, self.template_name, context)

        return HttpResponseRedirect(self.success_url)
    



# Tela Alteração das Unidades
class UnidadesUpdateViews(View):
    template_name = 'unidades/unidades_update.html'
    success_url = reverse_lazy("unidades_list")

    def get_context_data(self, **kwargs):
        context = {}
        user_condominio = self.request.user.n_condominio
        
        # Step 1: Get the blocos related to the user's condominium
        unidades = CustomUnidade.objects.filter(n_condominio=user_condominio)
        bloco_ids = unidades.values_list('bloco_id', flat=True).distinct()
        context['blocos'] = CustomBloco.objects.filter(bloco_id__in=bloco_ids)
        context['messages'] = messages.get_messages(self.request) 
        # Step 2: If a primary key is provided, fetch the unidade
        if 'pk' in kwargs:
            context['unidade'] = get_object_or_404(CustomUnidade, unidade_id=kwargs['pk'])
        
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(pk=kwargs['pk'])
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        unidade = get_object_or_404(CustomUnidade, unidade_id=kwargs['pk'])

        bloco_id = request.POST.get('bloco_id')
        unidade_str = request.POST.get('unidade')

        context = self.get_context_data(pk=kwargs['pk'])

        # Validar CPF do condômino
        condomino_instances = CustomCondomino.objects.filter(cpf_condomino=unidade.cpf_condomino.cpf_condomino)
        
        if not condomino_instances.exists():
            context['form_errors'] = {'CPF do condômino não cadastrado'}
            return render(request, self.template_name, context)
        
        # Obter a instância do condomínio associada ao condômino
        condominio_instance = request.user.n_condominio
        
        # Validar se a unidade já existe para o bloco
        if CustomUnidade.objects.filter(bloco_id=bloco_id, unidade=unidade_str, n_condominio=condominio_instance).exists():
            context['form_errors'] = {'Unidade já cadastrada para este bloco'}
            context['unidade'] = unidade  # Certificar-se de que a unidade está no contexto
            return render(request, self.template_name, context)

        # Atualizar a unidade existente
        unidade.bloco_id = CustomBloco.objects.get(bloco_id=bloco_id)
        unidade.unidade = unidade_str
        unidade.n_condominio = condominio_instance
        unidade.save()        
        return HttpResponseRedirect(self.success_url)
      



# Tela Exclusão das Unidades
class UnidadesDeleteViews(DeleteView):
    model = CustomUnidade
    success_url = reverse_lazy("unidades_list")
     
   



#-----------------------Views Veículos.................................................................

# Tela Lista Veículos 
class VeiculosListViews(LoginRequiredMixin, ListView):
    model = CustomVeiculo
    context_object_name = 'veiculo_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os veículos pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['veiculo_list'] = CustomVeiculo.objects.filter(n_condominio=user_condominio)
        
        return context
    
    



# Tela Cadastro de Veículos
@method_decorator(login_required, name='dispatch')
class VeiculosCreateViews(View):
    template_name = 'veiculos/veiculos_create.html'
    success_url = reverse_lazy("veiculos_list")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, *args, **kwargs):
        context = {}
        form_errors = {}

        cpf_condomino = request.POST.get('cpf_condomino')
        placa_veiculo = request.POST.get('placa_veiculo')
        marca_veiculo = request.POST.get('marca_veiculo')
        modelo_veiculo = request.POST.get('modelo_veiculo')
        cor_veiculo = request.POST.get('cor_veiculo')

        # Validar CPF do condômino
        try:
            user_condominio = self.request.user.n_condominio
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino, n_condominio=user_condominio)
        except CustomCondomino.DoesNotExist:
            messages.error(self.request, 'Condômino não cadastrado.')
            return render(request, self.template_name, context)
       
        # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        # Validar se o veículo já está cadastrado
        if CustomVeiculo.objects.filter(placa_veiculo=placa_veiculo, n_condominio=user_condominio_instance).exists():
            messages.error(self.request, 'Veículo já cadastrado.')
            return render(request, self.template_name, context)

        # Inserir os dados na tabela CustomVeiculo
        try:
            veiculo = CustomVeiculo(
                cpf_condomino=condomino_instance,
                placa_veiculo=placa_veiculo,
                marca_veiculo=marca_veiculo,
                modelo_veiculo=modelo_veiculo,
                cor_veiculo=cor_veiculo,
                n_condominio=user_condominio_instance
            )
            veiculo.save()
        except Exception as e:
            messages.error(self.request, 'Erro ao inserir o veículo.')
            return render(request, self.template_name, context)

        return redirect(self.success_url)



# Tela Alteração de Veículos
class VeiculosUpdateViews(View):
    template_name = 'veiculos/veiculos_update.html'
    success_url = reverse_lazy("veiculos_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['veiculo'] = kwargs.get('veiculo')
        return context

    def get(self, request, *args, **kwargs):
        veiculo_id = kwargs.get('pk')  # Obtenha o ID do veículo da URL
        try:
            veiculo = CustomVeiculo.objects.get(pk=veiculo_id)  
        except CustomVeiculo.DoesNotExist:
            messages.error(request, 'Tabela veículo não encontrada.')
            return redirect(self.success_url)

        context = self.get_context_data(veiculo=veiculo)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        veiculo_id = kwargs.get('pk')
        try:
            veiculo = CustomVeiculo.objects.get(pk=veiculo_id)
        except CustomVeiculo.DoesNotExist:
            messages.error(request, 'Tabela veículo não encontrada.')
            return redirect(self.success_url)

        # Obtenção dos dados do formulário
        cpf_condomino = request.POST.get('cpf_condomino')
        placa_veiculo = request.POST.get('placa_veiculo')
        marca_veiculo = request.POST.get('marca_veiculo')
        modelo_veiculo = request.POST.get('modelo_veiculo')
        cor_veiculo = request.POST.get('cor_veiculo')

        # Validar CPF do condômino
        try:
            # Obtém o n_condominio do usuário logado
            user_condominio_instance = request.user.n_condominio
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino, n_condominio=user_condominio_instance)
        except CustomCondomino.DoesNotExist:
            messages.error(self.request, 'Condômino não cadastrado.')
            context = self.get_context_data(veiculo=veiculo)
            return render(request, self.template_name, context)

        # Atualiza os dados do veículo
        veiculo.placa_veiculo = placa_veiculo
        veiculo.marca_veiculo = marca_veiculo
        veiculo.modelo_veiculo = modelo_veiculo
        veiculo.cor_veiculo = cor_veiculo
        veiculo.cpf_condomino = condomino_instance
        veiculo.n_condominio = request.user.n_condominio

        try:
            veiculo.save()
            messages.success(request, 'Veículo atualizado com sucesso.')
        except Exception as e:
            messages.error(request, 'Erro ao atualizar o veículo.')
            context = self.get_context_data(veiculo=veiculo)
            return render(request, self.template_name, context)

        return redirect(self.success_url)
    



# Tela Exclusão de Veículo
class VeiculosDeleteViews(DeleteView):
    model = CustomVeiculo
    success_url = reverse_lazy("veiculos_list")



#-----------------------Views Colaborador.................................................................

# Tela Lista Colaborador
class ColaboradoresListViews(LoginRequiredMixin, ListView):
    model = CustomColaborador
    context_object_name = 'colaboradores_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os colaboradores pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['colaboradores_list'] = CustomColaborador.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro de Colaborador 
@method_decorator(login_required, name='dispatch')
class ColaboradoresCreateViews(View):
    template_name = 'template_name.html'  # Defina o template aqui
    success_url = reverse_lazy("colaboradores_list")

    def get(self, request, *args, **kwargs):
        # Renderize o formulário vazio na requisição GET
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        context = {}  
        # Obtendo a instância do condomínio
        user_condominio_instance = get_object_or_404(CustomCondominio, pk=request.user.n_condominio.n_condominio)

        # Captura os dados do formulário e remove caracteres especiais de CPF e telefone
        cpf_colaborador = request.POST.get('cpf_colaborador', '').replace('.', '').replace('-', '')
        nome_colaborador = request.POST.get('nome_colaborador', '')
        data_nascimento_colaborador = request.POST.get('data_nascimento_colaborador', '').replace('-', '')
        endereco_colaborador = request.POST.get('endereco_colaborador', '')
        telefone_colaborador = request.POST.get('telefone_colaborador', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        celular_colaborador = request.POST.get('celular_colaborador', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        email_colaborador = request.POST.get('email_colaborador', '')
        nome_contato_colaborador = request.POST.get('nome_contato_colaborador', '')
        celular_contato_colaborador = request.POST.get('celular_contato_colaborador', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

        # Cria a instância do colaborador
        try:
            if CustomColaborador.objects.filter(cpf_colaborador=cpf_colaborador, n_condominio=user_condominio_instance).exists():
                messages.error(request, 'Colaborador já cadastrado.')
                return render(request, self.template_name, context)
            else:
                colaborador = CustomColaborador.objects.create(
                    cpf_colaborador=cpf_colaborador,
                    nome_colaborador=nome_colaborador,
                    data_nascimento_colaborador=data_nascimento_colaborador,
                    endereco_colaborador=endereco_colaborador,
                    telefone_colaborador=telefone_colaborador,
                    celular_colaborador=celular_colaborador,
                    email_colaborador=email_colaborador,
                    nome_contato_colaborador=nome_contato_colaborador,
                    celular_contato_colaborador=celular_contato_colaborador,
                    n_condominio=user_condominio_instance
                )                
        except IntegrityError as e:
            context['form_errors'] = 'Erro ao cadastrar: conflito de dados.'
            return render(request, self.template_name, context)
        except Exception as e:
            context['form_errors'] = f'Erro inesperado: {e}'
            return render(request, self.template_name, context)

        return HttpResponseRedirect(self.success_url)



# Tela Alteração De Colaborador
class ColaboradoresUpdateViews(UpdateView):
    model = CustomColaborador
    template_name = 'colaboradores/colaboradores_update.html'
    context_object_name = 'colaborador'
    fields = ["cpf_colaborador", "nome_colaborador", "data_nascimento_colaborador", "endereco_colaborador", "telefone_colaborador", "celular_colaborador", "email_colaborador", "nome_contato_colaborador", "celular_contato_colaborador"]
    success_url = reverse_lazy("colaboradores_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        cpf_colaborador = kwargs.get('pk')  # Obtem o cpf_colaborador da URL
        try:
            self.object = CustomColaborador.objects.get(pk=cpf_colaborador)  # Define self.object manualmente
        except CustomColaborador.DoesNotExist:
            messages.error(request, 'Colaborador inexistemte.')
            return redirect(self.success_url)

        context = self.get_context_data(object=self.object)  # Passa self.object para o contexto
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        cpf_colaborador = kwargs.get('pk')  # Obtém o CPF da URL
        try:
            self.object = CustomColaborador.objects.get(pk=cpf_colaborador)  # Define self.object manualmente
        except CustomColaborador.DoesNotExist:
            messages.error(request, 'Colaborador inexistemte.')
            return redirect(self.success_url)

        # Remove caracteres especiais de CPF e telefone
        cpf_colaborador = request.POST.get('cpf_colaborador', '').replace('.', '').replace('-', '')
        nome_colaborador = request.POST.get('nome_colaborador', '')
        data_nascimento_colaborador = request.POST.get('data_nascimento_colaborador', '').replace('-', '')
        endereco_colaborador = request.POST.get('endereco_colaborador', '')
        telefone_colaborador = request.POST.get('telefone_colaborador', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        celular_colaborador = request.POST.get('celular_colaborador', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        email_colaborador = request.POST.get('email_colaborador', '')
        nome_contato_colaborador = request.POST.get('nome_contato_colaborador', '')
        celular_contato_colaborador = request.POST.get('celular_contato_colaborador', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

        # Atualiza os campos da instância
        self.object.nome_colaborador = nome_colaborador
        self.object.data_nascimento_colaborador = data_nascimento_colaborador
        self.object.endereco_colaborador = endereco_colaborador
        self.object.telefone_colaborador = telefone_colaborador
        self.object.celular_colaborador = celular_colaborador
        self.object.email_colaborador = email_colaborador
        self.object.nome_contato_colaborador = nome_contato_colaborador
        self.object.celular_contato_colaborador = celular_contato_colaborador

        try:
            self.object.save()  # Salva a instância específica
        except IntegrityError:
            messages.error(request, 'Erro ao atualizar os dados do colaborador.')
            return render(request, self.template_name, {'colaborador': self.object})

        return HttpResponseRedirect(self.success_url)
        



# Tela Exclusão De Colaborador
class ColaboradoresDeleteViews(DeleteView):
    model = CustomColaborador
    success_url = reverse_lazy("colaboradores_list")



#-----------------------Views Garagens.................................................................

# Tela Lista Garagem
class GaragensListViews(LoginRequiredMixin, ListView):
    model = CustomGaragem
    context_object_name = 'garagens_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os garagens pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['garagens_list'] = CustomGaragem.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro Garagem
@method_decorator(login_required, name='dispatch')
class GaragensCreateViews(View):
    template_name = 'garagens/garagens_create.html'
    success_url = reverse_lazy("garagens_list")

    # Busca informações dos Blocos para o Select
    def get_context_data(self, **kwargs):
        context = {}
        user_condominio = self.request.user.n_condominio
        context['blocos'] = CustomBloco.objects.filter(n_condominio=user_condominio)
        context['messages'] = messages.get_messages(self.request) 

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        cpf_condomino = request.POST.get('cpf_condomino')
        bloco_id = request.POST.get('bloco_id')
        n_garagem = request.POST.get('n_garagem')

        context = self.get_context_data()
        
        # Obtendo a instância do condomínio
        user_condominio_instance = get_object_or_404(CustomCondominio, pk=request.user.n_condominio.n_condominio)

        # Validar CPF do condômino
        try:
            cpf_condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino, n_condominio=user_condominio_instance)
        except CustomCondomino.DoesNotExist:
            messages.error(request, 'Condômino não cadastrado.')
            return render(request, self.template_name, context)
        
        # Validar se a garagem já existe para o bloco
        if CustomGaragem.objects.filter(bloco_id=bloco_id, n_garagem=n_garagem, n_condominio=user_condominio_instance).exists():
            messages.error(request, 'Garagem já cadastrada para este bloco.')
            return render(request, self.template_name, context)

        # Criar a nova garagem
        try:
            garagem = CustomGaragem(
                cpf_condomino=cpf_condomino_instance,
                bloco_id=CustomBloco.objects.get(bloco_id=bloco_id),
                n_garagem=n_garagem,
                n_condominio=user_condominio_instance
            )        
            garagem.save()

        except Exception as e:
            messages.error(self.request, 'Erro ao inserir a garagem.')
            return render(request, self.template_name, context)

        return redirect(self.success_url)

    



# Tela Alteração Garagem
class GaragensUpdateViews(View):
    template_name = 'garagens/garagens_update.html'
    success_url = reverse_lazy("garagens_list")

    def get_context_data(self, **kwargs):
        context = {}
        user_condominio = self.request.user.n_condominio
        context['blocos'] = CustomBloco.objects.filter(n_condominio=user_condominio)
        context['messages'] = messages.get_messages(self.request) 
        if 'pk' in self.kwargs:
            context['garagem'] = CustomGaragem.objects.get(pk=self.kwargs['pk'])
        
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        cpf_condomino = request.POST.get('cpf_condomino')
        bloco_id = request.POST.get('bloco_id')
        n_garagem = request.POST.get('n_garagem')

        context = self.get_context_data()

        # Obtendo a instância do condomínio
        user_condominio_instance = get_object_or_404(CustomCondominio, pk=request.user.n_condominio.n_condominio)

        # Validar CPF do condômino
        try:
            cpf_condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino, n_condominio=user_condominio_instance)
        except CustomCondomino.DoesNotExist:
            messages.error(self.request, 'Condômino não cadastrado.')
            return render(request, self.template_name, context)

        # Validar se a garagem já existe para o bloco
        if CustomGaragem.objects.filter(bloco_id=bloco_id, n_garagem=n_garagem).exclude(pk=self.kwargs['pk']).exists():
            messages.error(self.request, 'Garagem já cadastrada para este bloco.')
            return render(request, self.template_name, context)

        # Atualizar a unidade existente
        try:
            # Carregue a garagem existente
            garagem = CustomGaragem.objects.get(pk=self.kwargs['pk'])
            garagem.cpf_condomino = cpf_condomino_instance
            garagem.bloco_id = CustomBloco.objects.get(bloco_id=bloco_id)
            garagem.n_garagem = n_garagem
            garagem.n_condominio = user_condominio_instance

            garagem.save()

        except CustomGaragem.DoesNotExist:
            messages.error(self.request, 'Garagem não encontrada.')
            return render(request, self.template_name, context)

        except Exception as e:
            messages.error(self.request, 'Erro ao alterar a garagem.')
            return render(request, self.template_name, context)

        return redirect(self.success_url)

    



# Tela Exclusão de Garagem
class GaragensDeleteViews(DeleteView):
    model = CustomGaragem
    success_url = reverse_lazy("garagens_list")



#-----------------------Views Mudanças.................................................................

# Tela Lista as Mudanças 
class MudancasListViews(LoginRequiredMixin, ListView):
    model = CustomMudanca
    context_object_name = 'mudancas_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar as mudanças pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['mudancas_list'] = CustomMudanca.objects.filter(n_condominio=user_condominio)
        
        return context



# Filtra as Unidades de um determinado Bloco p o select do creat e update
def filtrar_unidades(request):
    bloco_id = request.GET.get('bloco_id')
    if (bloco_id):
        unidades = CustomUnidade.objects.filter(bloco_id=bloco_id).values('unidade_id', 'unidade')
        return JsonResponse(list(unidades), safe=False)
    return JsonResponse({'error': 'Bloco não encontrado'}, status=400)



# Tela Cadastro de Mudanças
@method_decorator(login_required, name='dispatch')
class MudancasCreateViews(View):
    template_name = 'mudancas/mudancas_create.html'
    success_url = reverse_lazy("mudancas_list")

    def get_context_data(self, **kwargs):
        context = {}
        user_condominio = self.request.user.n_condominio
        context['blocos'] = CustomBloco.objects.filter(n_condominio=user_condominio)
        context['unidades'] = CustomUnidade.objects.filter(n_condominio=user_condominio)
        context['messages'] = messages.get_messages(self.request) 

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print('Entrei no post')
        cpf_condomino = request.POST.get('cpf_condomino')
        bloco_id = request.POST.get('bloco_id')
        unidade_id = request.POST.get('unidade_id')
        data_mudanca = request.POST.get('data_mudanca')
        hora_mudanca = request.POST.get('hora_mudanca')
        transportadora = request.POST.get('transportadora')

        context = self.get_context_data()
        
        # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        # Validar CPF do condômino
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino, n_condominio=user_condominio_instance)
        except CustomCondomino.DoesNotExist:
            messages.error(request, 'Condômino não cadastrado')
            return render(request, self.template_name, context)
      
        # Insere na tabela mudança nova linha
        CustomMudanca.objects.create(
            cpf_condomino=condomino_instance,
            bloco_id=CustomBloco.objects.get(bloco_id=bloco_id),
            unidade_id=CustomUnidade.objects.get(unidade_id=unidade_id),
            data_mudanca=data_mudanca,
            hora_mudanca=hora_mudanca,
            transportadora=transportadora,
            placa_veiculo_transportadora=request.POST.get('placa_veiculo_transportadora'),
            n_condominio=user_condominio_instance,
        )
        return HttpResponseRedirect(self.success_url)



# Tela Alteração das Mudanças
class MudancasUpdateViews(UpdateView):
    model = CustomMudanca
    template_name = 'mudancas/mudancas_update.html'
    context_object_name = 'mudanca'
    fields = [
        "cpf_condomino", "bloco_id", "unidade_id", "data_mudanca", "hora_mudanca", "transportadora", "placa_veiculo_transportadora"
    ]
    success_url = reverse_lazy("mudancas_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['condominios'] = CustomCondominio.objects.filter(n_condominio=user_condominio)
        user_condominio = self.request.user.n_condominio
        context['blocos'] = CustomBloco.objects.filter(n_condominio=user_condominio)
        context['unidades'] = CustomUnidade.objects.filter(n_condominio=user_condominio)
        mudanca = self.get_object()
        context['cpf_condomino'] = mudanca.cpf_condomino  # Adiciona o CPF do condômino no contexto
        context['messages'] = messages.get_messages(self.request) 
        
        return context

    def post(self, request, *args, **kwargs):
        # Carregar a instância de CustomMudanca
        self.object = self.get_object()  # Define o self.object corretamente
        
        # Obter os dados do formulário
        cpf_condomino_value = request.POST.get('cpf_condomino')
        user_condominio = request.user.n_condominio  # Pega o condomínio do usuário logado

        # Buscar o condômino pelo CPF e condomínio do usuário logado
        cpf_condomino_instance = get_object_or_404(CustomCondomino, cpf_condomino=cpf_condomino_value, n_condominio=user_condominio)
        
        bloco_id_value = request.POST.get('bloco_id')
        bloco_id_instance = get_object_or_404(CustomBloco, pk=bloco_id_value)  # Buscar a instância correta de CustomBloco

        unidade_id_value = request.POST.get('unidade_id')
        unidade_id_instance = get_object_or_404(CustomUnidade, pk=unidade_id_value)  # Buscar a instância correta de CustomUnidade
        
        data_mudanca = request.POST.get('data_mudanca')
        hora_mudanca = request.POST.get('hora_mudanca')
        transportadora = request.POST.get('transportadora')
        placa_veiculo_transportadora = request.POST.get('placa_veiculo_transportadora')

        # Atualizar os campos da mudança
        self.object.cpf_condomino = cpf_condomino_instance  # Usa a instância de CustomCondomino
        self.object.bloco_id = bloco_id_instance  # Usa a instância de CustomBloco
        self.object.unidade_id = unidade_id_instance  # Usa a instância de CustomUnidade
        self.object.data_mudanca = data_mudanca
        self.object.hora_mudanca = hora_mudanca
        self.object.transportadora = transportadora
        self.object.placa_veiculo_transportadora = placa_veiculo_transportadora
        self.object.n_condominio = request.user.n_condominio  # Usa o condomínio do usuário logado

        try:
            self.object.save()  # Salvar a instância de mudanca
        except Exception as e:
            messages.error(request, 'Erro ao alterar a mudança')
            context = self.get_context_data()
            return render(request, self.template_name, context)

        return redirect(self.success_url)

    



# Tela Exclusão das Mudanças
class MudancasDeleteViews(DeleteView):
    model = CustomMudanca
    success_url = reverse_lazy("mudancas_list")



#-----------------------Views Ocorrências.................................................................

# Tela Lista as Ocorrências 
class OcorrenciasListViews(LoginRequiredMixin, ListView):
    model = CustomOcorrencia
    context_object_name = 'ocorrencias_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar as ocorrencias pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['ocorrencias_list'] = CustomOcorrencia.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro de Ocorrências
@method_decorator(login_required, name='dispatch')
class OcorrenciasCreateViews(View):
    template_name = 'ocorrencias/ocorrencias_create.html'
    success_url = reverse_lazy("ocorrencias_list")
    
    def get_context_data(self, **kwargs):
        context = {}   
        context['messages'] = messages.get_messages(self.request) 

        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        cpf_condomino = request.POST.get('cpf_condomino')
        data_ocorrencia = request.POST.get('data_ocorrencia')
        hora_ocorrencia = request.POST.get('hora_ocorrencia')
        dsc_ocorrencia = request.POST.get('dsc_ocorrencia')
        documento_ocorrencia = request.FILES.get('documento_ocorrencia')
        
        context = self.get_context_data()
        
        # Obter o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio
        
        # Obter a instância do condômino associada ao ID do condômino
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino, n_condominio=user_condominio_instance)
        except CustomCondomino.DoesNotExist:
            messages.error(self.request, 'Condômino não encontrado.')
            return render(request, self.template_name, context)
        
       # Inserir os dados na tabela CustomOcorrência
        try:
            ocorrencia = CustomOcorrencia(
                cpf_condomino=condomino_instance,
                data_ocorrencia=data_ocorrencia,
                hora_ocorrencia=hora_ocorrencia,
                dsc_ocorrencia=dsc_ocorrencia,
                documento_ocorrencia=documento_ocorrencia,
                n_condominio=user_condominio_instance 
            )
            ocorrencia.save()
        except Exception as e:
            messages.error(self.request, 'Erro ao inserir a ocorrência.')
            return render(request, self.template_name, context)

        return redirect(self.success_url)



# Tela Alteração das Ocorrências
class OcorrenciasUpdateViews(UpdateView):
    model = CustomOcorrencia
    template_name = 'ocorrencias/ocorrencias_update.html'
    context_object_name = 'ocorrencia'
    fields = [ "cpf_condomino", "data_ocorrencia", "hora_ocorrencia", "dsc_ocorrencia", "documento_ocorrencia" ]
    success_url = reverse_lazy("ocorrencias_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request) 

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Recupera a instância existente da ocorrência
        context = self.get_context_data()
        
        cpf_condomino = request.POST.get('cpf_condomino')
        data_ocorrencia = request.POST.get('data_ocorrencia')
        hora_ocorrencia = request.POST.get('hora_ocorrencia')
        dsc_ocorrencia = request.POST.get('dsc_ocorrencia')
        documento_ocorrencia = request.FILES.get('documento_ocorrencia')  # Arquivos enviados são acessados com request.FILES
        
        # Obter o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        # Obter a instância do condômino associada ao CPF do condômino
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino, n_condominio=user_condominio_instance)
        except CustomCondomino.DoesNotExist:
            messages.error(self.request, 'Condômino não encontrado.')
            return render(request, self.template_name, context)

        # Atualizar os dados da ocorrência com a instância existente
        self.object.cpf_condomino = condomino_instance
        self.object.data_ocorrencia = data_ocorrencia
        self.object.hora_ocorrencia = hora_ocorrencia
        self.object.dsc_ocorrencia = dsc_ocorrencia
        
        # Verificar se um novo arquivo foi enviado
        if documento_ocorrencia:
            self.object.documento_ocorrencia = documento_ocorrencia  # Substitui o arquivo apenas se um novo for enviado
        
        # Obter o n_condominio do usuário logado
        self.object.n_condominio = request.user.n_condominio
        
        try:
            self.object.save()
            messages.success(self.request, 'Ocorrência atualizada com sucesso.')
            return redirect(self.success_url)
        except Exception as e:
            messages.error(self.request, 'Erro ao alterar a ocorrência.')
            return render(request, self.template_name, context)



# Tela Exclusão das Ocorrências
class OcorrenciasDeleteViews(DeleteView):
    model = CustomOcorrencia
    success_url = reverse_lazy("ocorrencias_list")



#-----------------------Views Benefícios.................................................................

# Tela Lista os Benefícios 
class BeneficiosListViews(LoginRequiredMixin, ListView):
    model = CustomBeneficio
    context_object_name = 'beneficios_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os bemefícios pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['beneficios_list'] = CustomBeneficio.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro de Benefícios
@method_decorator(login_required, name='dispatch')
class BeneficiosCreateViews(View):
    template_name = 'beneficios/beneficios_create.html'
    success_url = reverse_lazy("beneficios_list")

    def get_context_data(self, **kwargs):
        context = {}   
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    # Estrutura as informações para inserir na tabela nova linha
    def post(self, request, *args, **kwargs):
        nome_beneficio = request.POST.get('nome_beneficio')
        context = self.get_context_data()

        # Obter o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio   

    # Criar linha na tabela beneficio com o n_condominio do usuário logado
        try:
            if user_condominio_instance:
              CustomBeneficio.objects.create(
                    nome_beneficio=nome_beneficio,       
                    n_condominio= user_condominio_instance
        )
        except IntegrityError:
            messages.error(self.request, 'Ocorreu erro ao cadastrar.')
            return render(request, self.template_name, context)
        except Exception as e:
            messages.error(self.request, 'Ocorreu erro inesperado.')
            return render(request, self.template_name, context)

        return HttpResponseRedirect(self.success_url)



# Tela Alteração dos Benefícios
class BeneficiosUpdateViews(UpdateView):
    model = CustomBeneficio
    template_name = 'beneficios/beneficios_update.html'
    context_object_name = 'beneficio'
    fields = ["nome_beneficio", "n_condominio"]
    success_url = reverse_lazy("beneficios_list")

    # Recebe as informações do formulário
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Obtém o objeto a ser atualizado
        nome_beneficio = request.POST.get('nome_beneficio')
        context = self.get_context_data()

        # Obter o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio   

        # Atualizar a linha na tabela beneficio com o n_condominio do usuário logado
        try:
            if user_condominio_instance:
                self.object.nome_beneficio = nome_beneficio
                self.object.n_condominio = user_condominio_instance
                self.object.save()  # Salva as mudanças no banco de dados
        except IntegrityError:
            messages.error(self.request, 'Ocorreu erro ao alterar.')
            return render(request, self.template_name, context)
        except Exception as e:
            messages.error(self.request, 'Ocorreu erro inesperado.')
            return render(request, self.template_name, context)

        return HttpResponseRedirect(self.success_url)
    



# Tela Exclusão de Benefícios
class BeneficiosDeleteViews(DeleteView):
    model = CustomBeneficio
    success_url = reverse_lazy("beneficios_list")  



#-----------------------Views Benefícios recebidos pelos colaboradores....................................

# Tela Lista os Benefícios recebidos
class BeneficiosRecebidosListViews(LoginRequiredMixin, ListView):
    model = CustomBeneficioRecebido
    context_object_name = 'beneficios_recebidos_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os benefícios recebidos pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['beneficios_recebidos_list'] = CustomBeneficioRecebido.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro de Benefícios recebidos
@method_decorator(login_required, name='dispatch')
class BeneficiosRecebidosCreateViews(View):
    template_name = 'beneficios_recebidos/beneficios_recebidos_create.html'
    success_url = reverse_lazy("beneficios_recebidos_list")
    
    def get_context_data(self, **kwargs):
        context = {}
        context['beneficios'] = CustomBeneficio.objects.filter(n_condominio=self.request.user.n_condominio)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        cpf_colaborador_id = request.POST.get('cpf_colaborador')
        beneficio_id = request.POST.get('beneficio_id')
        context = self.get_context_data()

        # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        try:
            colaborador_instance = CustomColaborador.objects.get(cpf_colaborador=cpf_colaborador_id, n_condominio=user_condominio_instance)
        except CustomColaborador.DoesNotExist:
            context['form_errors'] = 'Colaborador inexistente.'
            return render(request, self.template_name, context)

        try:
            beneficio_instance = CustomBeneficio.objects.get(pk=beneficio_id, n_condominio=user_condominio_instance)
        except CustomBeneficio.DoesNotExist:
            context['form_errors'] = 'Benefício inexistente.'
            return render(request, self.template_name, context)

        # Cria linha na tabela
        try:
            CustomBeneficioRecebido.objects.create(
                cpf_colaborador=colaborador_instance,
                beneficio_id=beneficio_instance,
                n_condominio=user_condominio_instance
            )
        except IntegrityError:
            context['form_errors'] = 'Erro ao cadastrar'
            return render(request, self.template_name, context)
        except Exception as e:
            context['form_errors'] = f'Ocorreu erro inesperado: {str(e)}'
            return render(request, self.template_name, context)

        return HttpResponseRedirect(self.success_url)



# Tela Alteração dos Benefícios recebidos
class BeneficiosRecebidosUpdateViews(UpdateView):
    model = CustomBeneficioRecebido
    template_name = 'beneficios_recebidos/beneficios_recebidos_update.html'
    context_object_name = 'beneficio_recebido'
    fields = ["cpf_colaborador", "beneficio_id", "n_condominio"]
    success_url = reverse_lazy("beneficios_recebidos_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficios'] = CustomBeneficio.objects.all()  # Disponibiliza todos os benefícios no contexto
        return context

    def get(self, request, *args, **kwargs):
        beneficio_recebido_id = kwargs.get('pk')  # Obtém o benefício recebido pelo ID da URL

        try:
            self.object = CustomBeneficioRecebido.objects.get(pk=beneficio_recebido_id)  # Busca o benefício recebido
        except CustomBeneficioRecebido.DoesNotExist:
            messages.error(request, 'Benefício recebido inexistente.')
            return redirect(self.success_url)

        context = self.get_context_data(object=self.object)  # Passa o objeto para o contexto
        return render(request, self.template_name, context)

    from django.db import IntegrityError

    def post(self, request, *args, **kwargs):
        beneficio_recebido_id = kwargs.get('pk')  # Obtém o ID do benefício recebido a ser atualizado
        self.object = CustomBeneficioRecebido.objects.get(pk=beneficio_recebido_id)

        beneficio_id = request.POST.get('beneficio_id')  # Obtém o ID do benefício enviado pelo formulário
        cpf_colaborador = request.POST.get('cpf_colaborador')  # Obtém o CPF do colaborador enviado pelo formulário
                
        user_condominio_instance = request.user.n_condominio # Obtém o n_condominio do usuário logado

        try:
            # Busca a instância de CustomBeneficio com base no beneficio_id fornecido
            beneficio = CustomBeneficio.objects.get(pk=beneficio_id)
            self.object.beneficio_id = beneficio  # Atribui a instância de CustomBeneficio

            # Busca a instância de CustomColaborador com base no campo cpf_colaborador correto
            colaborador = CustomColaborador.objects.get(cpf_colaborador=cpf_colaborador)
            self.object.cpf_colaborador = colaborador  # Atribui a instância de CustomColaborador

            # Atualiza outros campos, se necessário
            # user_condominio_instance = request.user.n_condominio # Obtém o n_condominio do usuário logado
            self.object.n_condominio = request.user.n_condominio 

            self.object.save()  # Salva o objeto atualizado
        except CustomBeneficio.DoesNotExist:
            messages.error(request, 'O benefício selecionado não existe.')
            return render(request, self.template_name, {'beneficio_recebido': self.object})
        except CustomColaborador.DoesNotExist:
            messages.error(request, 'O colaborador com o CPF fornecido não existe.')
            return render(request, self.template_name, {'beneficio_recebido': self.object})
        except IntegrityError as e:
            # Exibe a mensagem detalhada do erro de integridade
            messages.error(request, f'Erro ao atualizar os benefícios recebidos: {e}')
            return render(request, self.template_name, {'beneficio_recebido': self.object})
        except Exception as e:
            # Captura qualquer outra exceção inesperada
            messages.error(request, f'Ocorreu um erro inesperado: {e}')
            return render(request, self.template_name, {'beneficio_recebido': self.object})

        return HttpResponseRedirect(self.success_url)



# Tela Exclusão dos Benefícios recebidos
class BeneficiosRecebidosDeleteViews(DeleteView):
    model = CustomBeneficioRecebido
    success_url = reverse_lazy("beneficios_recebidos_list")

   



#-----------------------Views Correspondências .................................................................

# Tela Lista as Correspondencias por Bloco e Unidade
class CorrespondenciasListViews(LoginRequiredMixin, ListView):
    model = CustomCorrespondencia
    context_object_name = 'correspondencias_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar as correspondências pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['correspondencias_list'] = CustomCorrespondencia.objects.filter(n_condominio=user_condominio, data_retirada_correspondencia__isnull=True)
        
        return context



# Tela Cadastra as Correspondencias por Bloco e Unidade
@method_decorator(login_required, name='dispatch')
class CorrespondenciasCreateViews(View):
    template_name = 'correspondencias/correspondencias_create.html'
    success_url = reverse_lazy("correspondencias_list")

    def get_context_data(self, **kwargs):
        context = {}
        # Filtrar as correspondências pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['blocos'] = CustomBloco.objects.filter(n_condominio=user_condominio)
        context['unidades'] = CustomUnidade.objects.filter(n_condominio=user_condominio)
        context['messages'] = messages.get_messages(self.request) 
        
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        bloco_id = request.POST.get('bloco_id')
        unidade_id = request.POST.get('unidade_id')
        dsc_correspondencia = request.POST.get('dsc_correspondencia')
        data_recebimento_correspondencia = request.POST.get('data_recebimento_correspondencia')

        user_condominio_instance = request.user.n_condominio        

        try:
            CustomCorrespondencia.objects.create(
                bloco_id=CustomBloco.objects.get(bloco_id=bloco_id),
                unidade_id=CustomUnidade.objects.get(unidade_id=unidade_id),
                dsc_correspondencia=dsc_correspondencia,
                data_recebimento_correspondencia=data_recebimento_correspondencia,
                n_condominio=user_condominio_instance
            )
            return redirect(self.success_url)
        
        except Exception as e:
            context = self.get_context_data()
            context['form_errors'] = 'Preencha os campos corretamente.'
            context.update(request.POST.dict())  # Adiciona os valores submetidos ao contexto para manter os dados no template

            return render(request, self.template_name, context)



# Tela Alteração das Correspondencias por Bloco e Unidade
class CorrespondenciasUpdateViews(UpdateView):
    model = CustomCorrespondencia
    template_name = 'correspondencias/correspondencias_update.html'
    context_object_name = 'correspondencia'
    fields = [
         "bloco_id", "unidade_id", "data_recebimento_correspondencia", "dsc_correspondencia"
    ]
    success_url = reverse_lazy("correspondencias_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_condominio = self.request.user.n_condominio
        context['blocos'] = CustomBloco.objects.filter(n_condominio=user_condominio)
        context['unidades'] = CustomUnidade.objects.filter(n_condominio=user_condominio)
        context['messages'] = messages.get_messages(self.request) 
        return context

    def form_valid(self, form):
        # Obter o objeto CustomCondominio associado ao usuário logado
        user_condominio = self.request.user.n_condominio  # Isso já é o objeto CustomCondominio

        # Atribuir o objeto inteiro ao campo n_condominio
        form.instance.n_condominio = user_condominio

        bloco_instance = form.cleaned_data.get('bloco_id')
        unidade_instance = form.cleaned_data.get('unidade_id')

        # Validar o condomínio
        if not CustomCondominio.objects.filter(n_condominio=user_condominio.n_condominio).exists():
            messages.error(self.request, 'Condomínio inválido.')
            return self.form_invalid(form)
        
        # Validar o bloco
        if not CustomBloco.objects.filter(bloco_id=bloco_instance.bloco_id, n_condominio=user_condominio.n_condominio).exists():
            messages.error(self.request, 'Bloco inexistente')
            return self.form_invalid(form)
        
        # Validar a unidade
        if not CustomUnidade.objects.filter(unidade_id=unidade_instance.unidade_id, bloco_id=bloco_instance.bloco_id, n_condominio=user_condominio.n_condominio).exists():
            messages.error(self.request, 'Unidade inexistente')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao alterar a correspondência.')

        return super().form_invalid(form)
    



# Tela Exclusão das Correspondencias por Bloco e Unidade
class CorrespondenciasDeleteViews(DeleteView):
    model = CustomCorrespondencia
    success_url = reverse_lazy("correspondencias_list")



# Tela Entrega de Correspondencia
class CorrespondenciasEntregarViews(UpdateView):
    model = CustomCorrespondencia
    template_name = 'correspondencias/correspondencias_entregar.html'
    context_object_name = 'correspondencia'
    fields = [
        "data_retirada_correspondencia", "retirante_correspondencia"
    ]
    success_url = reverse_lazy("correspondencias_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request) 
        
        return context

    def form_valid(self, form):
        # Obter o objeto CustomCondominio associado ao usuário logado
        user_condominio = self.request.user.n_condominio  

        # Atribuir o objeto inteiro ao campo n_condominio
        form.instance.n_condominio = user_condominio

        # Validar o condomínio
        if not CustomCondominio.objects.filter(n_condominio=user_condominio.n_condominio).exists():
            messages.error(self.request, 'Condomínio inválido.')
            return self.form_invalid(form)

        # Verificar se a data de retirada é maior que a data de recebimento
        data_retirada = form.cleaned_data.get('data_retirada_correspondencia')
        data_recebimento = form.instance.data_recebimento_correspondencia  # Supondo que este campo exista no modelo

        if data_retirada and data_recebimento:  # Verifica se as datas estão presentes
            if data_retirada < data_recebimento:
                messages.error(self.request, 'A data de retirada precisa ser maior ou igual a data do recebimento.')
                return self.form_invalid(form)

        return super().form_valid(form)



    def form_invalid(self, form):
        messages.error(self.request, 'Erro no cadastro de entrega da correspondência.')

        return super().form_invalid(form)



#-----------------------Views Espaços Administrativos .................................................................

# Tela Lista os Espaços adm   
class EspacosAdmListViews(LoginRequiredMixin, ListView):
    model = CustomEspacoAdm
    context_object_name = 'espacosAdm_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os espaços administrativos pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['espacosAdm_list'] = CustomEspacoAdm.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro dos Espaços Adm
@method_decorator(login_required, name='dispatch')
class EspacosAdmCreateViews(View):
    template_name = 'espacosAdm/espacosAdm_create.html'
    success_url = reverse_lazy("espacosAdm_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['messages'] = messages.get_messages(self.request) 

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        nome_espaco_adm = request.POST.get('nome_espaco_adm')

        # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        context = self.get_context_data()
        
        CustomEspacoAdm.objects.create(
            nome_espaco_adm=nome_espaco_adm,
            n_condominio=user_condominio_instance,
        )
        return HttpResponseRedirect(self.success_url)



# Tela Alteração de Espaços Adm
class EspacosAdmUpdateViews(UpdateView):
    model = CustomEspacoAdm
    template_name = 'espacosAdm/espacosAdm_update.html'
    context_object_name = 'espaco_adm'
    fields = ["nome_espaco_adm"]
    template_name = "espacoAdm/espacoAdm_update.html"
    success_url = reverse_lazy("espacosAdm_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request) 
    
        return context

    def post(self, request, *args, **kwargs):
            # Obtém o objeto existente
            self.object = self.get_object()

            nome_espaco_adm = request.POST.get('nome_espaco_adm')  

            context = self.get_context_data()

            # Obtém o n_condominio do usuário logado
            user_condominio_instance = request.user.n_condominio

            # Atualiza os atributos do objeto existente
            self.object.nome_espaco_adm = nome_espaco_adm
            self.object.n_condominio = user_condominio_instance

            # Tenta salvar os dados atualizados
            try:
                self.object.save()
            except Exception as e:
                messages.error(self.request, f'Erro ao alterar o espaço: {str(e)}')
                return render(request, self.template_name, context)

            return redirect(self.success_url)
    



# Tela Exclusão de Espaços Adm
class EspacosAdmDeleteViews(DeleteView):
    model = CustomEspacoAdm
    success_url = reverse_lazy("espacosAdm_list")



#-----------------------Views Tipos DE Patrimônio .................................................................

# Tela Lista os Tipos Patrimônio
class TiposPatrimonioListViews(LoginRequiredMixin, ListView):
    model = CustomTipoPatrimonio
    context_object_name = 'tiposPatrimonio_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os tipos de patimônio pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['tiposPatrimonio_list'] = CustomTipoPatrimonio.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro dos Tipos Patrimônio
@method_decorator(login_required, name='dispatch')
class TiposPatrimonioCreateViews(View):
    template_name = 'tiposPatrimonio/tiposPatrimonio_create.html'
    success_url = reverse_lazy("tiposPatrimonio_list")

    def get_context_data(self, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        nome_patrimonio = request.POST.get('nome_patrimonio')
        n_patrimonio = request.POST.get('n_patrimonio')
        cor_patrimonio = request.POST.get('cor_patrimonio')
        descricao_patrimonio = request.POST.get('descricao_patrimonio')   

        context = self.get_context_data()

      # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        tipo_patrimonio = CustomTipoPatrimonio (
            nome_patrimonio = nome_patrimonio,
            n_patrimonio = n_patrimonio,
            cor_patrimonio = cor_patrimonio,
            descricao_patrimonio = descricao_patrimonio,
            n_condominio=user_condominio_instance,
        )
        
        # Insere dados na tabela CustomTipoPatrimonio
        try:
            tipo_patrimonio.save()
        except Exception as e:
            messages.error(self.request, f'Erro ao inserir o tipo de patrimônio: {str(e)}')
            return render(request, self.template_name, context)

        return redirect(self.success_url)
    



# Tela Alteração dos Tipos Patrimônio
class TiposPatrimonioUpdateViews(UpdateView):
    model = CustomTipoPatrimonio
    template_name = 'tiposPatrimonio/tiposPatrimonio_update.html'
    context_object_name = 'tipo_patrimonio'
    fields = ["nome_patrimonio", "n_patrimonio", "cor_patrimonio","descricao_patrimonio"]
    success_url = reverse_lazy("tiposPatrimonio_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # Obtém o objeto existente
        self.object = self.get_object()

        nome_patrimonio = request.POST.get('nome_patrimonio')
        n_patrimonio = request.POST.get('n_patrimonio')
        cor_patrimonio = request.POST.get('cor_patrimonio')
        descricao_patrimonio = request.POST.get('descricao_patrimonio')   

        context = self.get_context_data()

        # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        # Atualiza os atributos do objeto existente
        self.object.nome_patrimonio = nome_patrimonio
        self.object.n_patrimonio = n_patrimonio
        self.object.cor_patrimonio = cor_patrimonio
        self.object.descricao_patrimonio = descricao_patrimonio
        self.object.n_condominio = user_condominio_instance

        # Tenta salvar os dados atualizados
        try:
            self.object.save()
        except Exception as e:
            messages.error(self.request, f'Erro ao inserir o tipo de patrimônio: {str(e)}')
            return render(request, self.template_name, context)

        return redirect(self.success_url)
    



# Tela Exclusão dos Tipos Patrimônio
class TiposPatrimonioDeleteViews(DeleteView):
    model = CustomTipoPatrimonio
    success_url = reverse_lazy("tiposPatrimonio_list")



#-----------------------Views DE Patrimônio .................................................................

# Tela Lista de Patrimônios
class PatrimonioListViews(ListView):
    model = CustomPatrimonio
    template_name = 'patrimonio/patrimonio_list.html'
    context_object_name = 'patrimonio_list'

  

    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)

        # Filtrar os patrimônios pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['patrimonio_list'] = CustomPatrimonio.objects.filter(
            n_condominio=user_condominio
        ).exclude(qtd_patrimonio=F('qtd_baixada_patrimonio'))  # Excluir registros onde qtd_patrimonio é igual a qtd_baixada_patrimonio

        return context  



# Tela Cadastro de Patrimônio
@method_decorator(login_required, name='dispatch')
class PatrimonioCreateViews(View):
    template_name = 'patrimonio/patrimonio_create.html'
    success_url = reverse_lazy("patrimonio_list")

    def get_context_data(self, **kwargs):
        context = {}
        user_condominio = self.request.user.n_condominio
        context['espacos'] = CustomEspacoAdm.objects.filter(n_condominio=user_condominio)
        context['tiposPatrimonio'] = CustomTipoPatrimonio.objects.filter(n_condominio=user_condominio)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form_data'] = {
            'tipo_patrimonio_id': '',
            'espaco_adm_id': '',
            'valor_patrimonio': '',
            'qtd_patrimonio': '',
            'data_disposicao_patrimonio': ''
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
 
        tipo_patrimonio_id = request.POST.get('tipo_patrimonio_id')
        espaco_adm_id = request.POST.get('espaco_adm_id')
        valor_patrimonio = request.POST.get('valor_patrimonio')
        qtd_patrimonio = int(request.POST.get('qtd_patrimonio'))
        data_disposicao_patrimonio = request.POST.get('data_disposicao_patrimonio')

        context = self.get_context_data()

        form_data = {
            'tipo_patrimonio_id': tipo_patrimonio_id,
            'espaco_adm_id': espaco_adm_id,
            'valor_patrimonio': valor_patrimonio,
            'qtd_patrimonio': qtd_patrimonio,
            'data_disposicao_patrimonio': data_disposicao_patrimonio,
        }
        context['form_data'] = form_data

        # Verifica se os IDs selecionados existem no banco de dados
        try:
            tipo_patrimonio_instance = CustomTipoPatrimonio.objects.get(pk=tipo_patrimonio_id)
            espaco_adm_instance = CustomEspacoAdm.objects.get(pk=espaco_adm_id)
        except CustomTipoPatrimonio.DoesNotExist:
            messages.error(self.request, 'Tipo de patrimônio inexistente.')
            return render(request, self.template_name, context)
        except CustomEspacoAdm.DoesNotExist:
            messages.error(self.request, 'Espaço administrativo inexistente.')
            return render(request, self.template_name, context)
        except:
            messages.error(self.request, 'Erro inesperado.')
            return render(request, self.template_name, context)
        
         # Valida a quantidade do patrimônio
        try:
            qtd_patrimonio = int(qtd_patrimonio)
            if qtd_patrimonio <= 0:
                messages.error(self.request, 'A quantidade do patrimônio tem que ser maior que 0.')
                return render(request, self.template_name, context)
        except ValueError:
            messages.error(self.request, 'Quantidade inválida.')
            return render(request, self.template_name, context)

        # Conversão de valor_patrimonio para Decimal
        try:
            valor_patrimonio = Decimal(valor_patrimonio.replace(',', '.'))
        except (ValueError, InvalidOperation):
            messages.error(self.request, 'Valor do patrimônio inválido.')
            return render(request, self.template_name, context)
                     
         # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        patrimonio = CustomPatrimonio (
            tipo_patrimonio_id=tipo_patrimonio_instance,
            espaco_adm_id=espaco_adm_instance,
            valor_patrimonio=valor_patrimonio,
            qtd_patrimonio=qtd_patrimonio,
            data_disposicao_patrimonio=data_disposicao_patrimonio,
            n_condominio=user_condominio_instance,
        )
            
        # Insere dados na tabela CustomPatrimônio
        try:
            patrimonio.save()
        except Exception as e:
            messages.error(self.request, f'Erro ao inserir o patrimônio: {str(e)}')
            return render(request, self.template_name, context)

        return redirect(self.success_url)
    



# Tela Alteração de Patrimônio
class PatrimonioUpdateViews(UpdateView):
    model = CustomPatrimonio
    template_name = 'patrimonio/patrimonio_update.html'
    context_object_name = 'patrimonio'
    fields = ["tipo_patrimonio_id", "espaco_adm_id", "valor_patrimonio", "qtd_patrimonio", "data_disposicao_patrimonio"]
    success_url = reverse_lazy("patrimonio_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patrimonio = self.get_object()  # Carrega o objeto corretamente
        user_condominio = self.request.user.n_condominio
        context['espacos'] = CustomEspacoAdm.objects.filter(n_condominio=user_condominio)
        context['tiposPatrimonio'] = CustomTipoPatrimonio.objects.filter(n_condominio=user_condominio)

        # Formatando as datas para o formato dd/mm/aa
        if patrimonio.data_disposicao_patrimonio:
            context['data_disposicao_patrimonio_formatada'] = DateFormat(patrimonio.data_disposicao_patrimonio).format(get_format('DATE_FORMAT'))
    
        # Formatando o valor do patrimônio para moeda brasileira
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        context['valor_patrimonio_formatado'] = f"{patrimonio.valor_patrimonio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
       
        return context

    def post(self, request, *args, **kwargs):        

        self.object = self.get_object()  # Obtém a instância existente

        tipo_patrimonio_id = request.POST.get('tipo_patrimonio_id')
        espaco_adm_id = request.POST.get('espaco_adm_id')
        valor_patrimonio = request.POST.get('valor_patrimonio')
        qtd_patrimonio = int(request.POST.get('qtd_patrimonio'))
        data_disposicao_patrimonio = request.POST.get('data_disposicao_patrimonio')

        context = self.get_context_data()

        # Converte a string para decimal
        try:
            valor_patrimonio = valor_patrimonio.replace('.', '').replace(',', '.')
            valor_patrimonio = Decimal(valor_patrimonio)
        except (ValueError, InvalidOperation):
            messages.error(self.request, 'Valor do patrimônio inválido.')
            return render(request, self.template_name, context)

        # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        # Verifica se os IDs selecionados existem no banco de dados
        try:
            tipo_patrimonio_instance = CustomTipoPatrimonio.objects.get(pk=tipo_patrimonio_id)
            espaco_adm_instance = CustomEspacoAdm.objects.get(pk=espaco_adm_id)

        except CustomTipoPatrimonio.DoesNotExist:
            messages.error(self.request, 'Tipo de patrimônio não encontrado.')
            return render(request, self.template_name, context)
        
        except CustomEspacoAdm.DoesNotExist:
            messages.error(self.request, 'Espaço administrativo não encontrado.')
            return render(request, self.template_name, context)
        
        except:
            messages.error(self.request, 'Erro inesperado.')
            return render(request, self.template_name, context)

        # Valida a quantidade do patrimônio
        if qtd_patrimonio <= 0:
            messages.error(self.request, 'A quantidade do patrimônio tem que ser maior que 0.')
            return render(request, self.template_name, context)

        # Atualiza a instância existente
        self.object.tipo_patrimonio_id = tipo_patrimonio_instance
        self.object.espaco_adm_id = espaco_adm_instance
        self.object.valor_patrimonio = valor_patrimonio
        self.object.qtd_patrimonio = qtd_patrimonio
        self.object.data_disposicao_patrimonio = data_disposicao_patrimonio
        self.object.n_condominio = user_condominio_instance

        try:            
            self.object.save()  # Salva a instância existente

        except Exception as e:
            messages.error(self.request, 'Erro ao alterar o patrimônio.')
            return render(request, self.template_name, context)

        return redirect(self.success_url)
    



# Tela Exclusão de Patrimônio
class PatrimonioDeleteViews(DeleteView):
    model = CustomPatrimonio
    success_url = reverse_lazy("patrimonio_list")



# Tela Baixa de Patrimônio

class PatrimonioBaixarViews(UpdateView):
    model = CustomPatrimonio
    template_name = 'patrimonio/patrimonio_update.html'
    context_object_name = 'patrimonio'
    fields = ["data_baixa_patrimonio", "qtd_baixada_patrimonio"]
    success_url = reverse_lazy("patrimonio_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patrimonio = self.get_object()
        user_condominio = self.request.user.n_condominio
        context['espacos'] = CustomEspacoAdm.objects.filter(n_condominio=user_condominio)
        context['tiposPatrimonio'] = CustomTipoPatrimonio.objects.filter(n_condominio=user_condominio)

        # Formata a data se existir
        if patrimonio.data_baixa_patrimonio:
            context['data_baixa_patrimonio_formatada'] = DateFormat(patrimonio.data_baixa_patrimonio).format(get_format('DATE_FORMAT'))

        # Mantenha os valores dos campos ao renderizar
        context['data_baixa_patrimonio'] = patrimonio.data_baixa_patrimonio
        context['qtd_baixada_patrimonio'] = patrimonio.qtd_baixada_patrimonio

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()

        # Obtém dados do formulário
        data_baixa_patrimonio_str = request.POST.get('data_baixa_patrimonio', '')
        qtd_baixada_patrimonio_str = request.POST.get('qtd_baixada_patrimonio', '')

        # Tenta converter a string da data para um objeto date
        try:
            data_baixa_patrimonio = datetime.strptime(data_baixa_patrimonio_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, 'Data de baixa inválida.')
            # Mantenha os valores digitados no contexto
            context['data_baixa_patrimonio'] = data_baixa_patrimonio_str
            context['qtd_baixada_patrimonio'] = qtd_baixada_patrimonio_str
            return render(request, self.template_name, context)

        # Validações dos campos
        if not data_baixa_patrimonio:
            messages.error(request, 'Informe a data de baixa.')
            # Mantenha os valores digitados no contexto
            context['data_baixa_patrimonio'] = data_baixa_patrimonio_str
            context['qtd_baixada_patrimonio'] = qtd_baixada_patrimonio_str
            return render(request, self.template_name, context)

        if qtd_baixada_patrimonio_str == '' or int(qtd_baixada_patrimonio_str) <= 0:
            messages.error(request, 'Informe uma quantidade válida a ser baixada.')
            # Mantenha os valores digitados no contexto
            context['data_baixa_patrimonio'] = data_baixa_patrimonio_str
            context['qtd_baixada_patrimonio'] = qtd_baixada_patrimonio_str
            return render(request, self.template_name, context)

        qtd_baixada_patrimonio = int(qtd_baixada_patrimonio_str)

        if qtd_baixada_patrimonio > self.object.qtd_patrimonio:
            messages.error(request, 'A quantidade baixada deve ser menor ou igual à quantidade alocada.')
            # Mantenha os valores digitados no contexto
            context['data_baixa_patrimonio'] = data_baixa_patrimonio_str
            context['qtd_baixada_patrimonio'] = qtd_baixada_patrimonio_str
            return render(request, self.template_name, context)

        # Valida a data de baixa em relação à data de disposição, se existir
        if self.object.data_disposicao_patrimonio and data_baixa_patrimonio < self.object.data_disposicao_patrimonio:
            messages.error(request, 'A data de baixa deve ser superior à data da alocação.')
            # Mantenha os valores digitados no contexto
            context['data_baixa_patrimonio'] = data_baixa_patrimonio_str
            context['qtd_baixada_patrimonio'] = qtd_baixada_patrimonio_str
            return render(request, self.template_name, context)

        # Atualiza os campos da instância
        self.object.data_baixa_patrimonio = data_baixa_patrimonio
        self.object.qtd_baixada_patrimonio = qtd_baixada_patrimonio
        self.object.n_condominio = request.user.n_condominio

        try:
            self.object.save()
            messages.success(request, 'Patrimônio atualizado com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao alterar o patrimônio: {str(e)}')
            return render(request, self.template_name, context)

        return redirect(self.success_url)






#-----------------------Views DE Espaços .................................................................

# Tela Lista de Espaços
class EspacosListViews(LoginRequiredMixin, ListView):
    model = CustomEspaco
    context_object_name = 'espacos_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os espaços pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['espacos_list'] = CustomEspaco.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro de Espaços
@method_decorator(login_required, name='dispatch')
class EspacosCreateViews(View):
    template_name = 'espacos/espacos_create.html'
    success_url = reverse_lazy("espacos_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['messages'] = messages.get_messages(self.request) 

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        nome_espaco = request.POST.get('nome_espaco')
        dsc_espaco = request.POST.get('dsc_espaco')
        tempo_espaco = request.POST.get('tempo_espaco')
        valor_espaco = request.POST.get('valor_espaco')
        
        # Formatar o valor do espaço antes de salvar
        try:
            # Primeiro, remover todos os pontos da string
            valor_espaco = valor_espaco.replace('.', '')

            # Em seguida, substituir a vírgula por um ponto
            valor_espaco = valor_espaco.replace(',', '.')

            # Agora, tentar converter para float
            valor_espaco = float(valor_espaco)
        except ValueError:
            context = self.get_context_data()
            context['form_errors'] = "O valor inserido para o campo Valor é inválido."

            return render(request, self.template_name, context)

        # Obter o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        CustomEspaco.objects.create(
            nome_espaco=nome_espaco,
            dsc_espaco=dsc_espaco,
            tempo_espaco=tempo_espaco,
            valor_espaco=valor_espaco,
            n_condominio=user_condominio_instance,
        )
        return HttpResponseRedirect(self.success_url)



# Tela Alteração de Espaços
class EspacosUpdateViews(UpdateView):
    model = CustomEspaco
    template_name = 'espacos/espacos_update.html'
    context_object_name = 'espaco'
    fields = ["nome_espaco", "dsc_espaco", "tempo_espaco", "valor_espaco"]
    success_url = reverse_lazy("espacos_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['espaco'] = self.get_object()
        context['messages'] = messages.get_messages(self.request) 
        
        return context

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response

    def form_valid(self, form):
        # Aqui você pode adicionar qualquer lógica adicional necessária antes de salvar o formulário
        return super().form_valid(form)
   



# Tela Exclusão de Espaços
class EspacosDeleteViews(DeleteView):
    model = CustomEspaco
    success_url = reverse_lazy("espacos_list")



#-----------------------Views De Reservas .................................................................

# Tela Lista de Reservas

class ReservasListViews(LoginRequiredMixin, ListView):
    model = CustomReserva
    context_object_name = 'reservas_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar as reservas pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['reservas_list'] = CustomReserva.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro de Reservas
class ReservasCreateViews(View):
    template_name = 'reservas/reservas_create.html'
    success_url = reverse_lazy("reservas_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['condominios'] = CustomCondominio.objects.all()
        context['espacos'] = CustomEspaco.objects.all()
        context['today'] = date.today().strftime('%Y-%m-%d')  # Adiciona a data de hoje ao contexto
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        cpf_morador_id = request.POST.get('cpf_morador', '').replace('.', '').replace('-', '').strip()
        espaco_id = request.POST.get('espaco_id')
        data_reserva = request.POST.get('data_reserva')
        hora_inicio_reserva = request.POST.get('hora_inicio_reserva')
        condominio_id = request.POST.get('n_condominio')
        context = self.get_context_data()

        try:
            espaco_instance = CustomEspaco.objects.get(pk=espaco_id)
            condominio_instance = CustomCondominio.objects.get(pk=condominio_id)

            morador_instance = None
            cpf_reserva = None

            if CustomMorador.objects.filter(cpf_morador=cpf_morador_id).exists():
                morador_instance = CustomMorador.objects.get(cpf_morador=cpf_morador_id)
                cpf_reserva = morador_instance.cpf_morador
            elif CustomMorador.objects.filter(cpf_condomino=cpf_morador_id).exists():
                morador_instance = CustomMorador.objects.get(cpf_condomino=cpf_morador_id)
                cpf_reserva = morador_instance.cpf_condomino
            else:
                context['error'] = "Morador inexistente no Condomínio"
                return render(request, self.template_name, context)

            if isinstance(cpf_reserva, str):
                cpf_reserva = cpf_reserva[:14]

                CustomReserva.objects.create(
                    cpf_reserva=cpf_reserva,
                    espaco_id=espaco_instance,
                    data_reserva=data_reserva,
                    hora_inicio_reserva=hora_inicio_reserva,
                    n_condominio=condominio_instance,
                )
                return HttpResponseRedirect(self.success_url)
            else:
                context['error'] = "O CPF obtido não é uma string válida"
                return render(request, self.template_name, context)

        except CustomEspaco.DoesNotExist:
            context['error'] = "Espaço para reserva inexistente"
            return render(request, self.template_name, context)

        except CustomCondominio.DoesNotExist:
            context['error'] = "Condomínio inexistente"
            return render(request, self.template_name, context)
        



# Tela Alteração de Reservas
class ReservasUpdateViews(UpdateView):
    model = CustomReserva
    template_name = 'reservas/reservas_update.html'
    context_object_name = 'reserva'
    fields = ["cpf_morador", "espaco_id", "data_reserva", "hora_inicio_reserva", "hora_fim_reserva", "n_condominio"]
    success_url = reverse_lazy("reservas_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
       
        return context

    # def form_valid(self, form):
    #     try:
    #         condominio_id = self.request.POST.get('n_condominio')
    #         if condominio_id:
    #             form.instance.n_condominio = CustomCondominio.objects.get(pk=condominio_id)
            
    #     except CustomCondominio.DoesNotExist:
    #         messages.error(self.request, 'Número de condomínio inválido.')
    #         return self.form_invalid(form)
        
        # Extrai as datas do formulário
        # nome_espaco = form.cleaned_data.get('nome_espaco')
        # dsc = form.cleaned_data.get('dsc')

        # return super().form_valid(form)    
    



# Tela Exclusão de Reservas
class ReservasDeleteViews(DeleteView):
    model = CustomReserva
    success_url = reverse_lazy("reservas_list")






  #-----------------------Views Pets.................................................................




# Tela Lista Pets 
class PetsListViews(LoginRequiredMixin, ListView):
    model = CustomPets
    context_object_name = 'pets_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os pets pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['pets_list'] = CustomPets.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro Pets
@method_decorator(login_required, name='dispatch')
class PetsCreateViews(View):
    template_name = 'pets/pets_create.html'
    success_url = reverse_lazy("pets_list")

    def get_context_data(self, **kwargs):
        context = {}
        user_condominio = self.request.user.n_condominio
        context['condominos'] = CustomCondomino.objects.filter(n_condominio=user_condominio)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Remove a máscara do CPF
        cpf_condomino_id = re.sub(r'\D', '', request.POST.get('cpf_condomino'))

        nome_pet = request.POST.get('nome_pet')
        raca_pet = request.POST.get('raca_pet')
        altura_pet = request.POST.get('altura_pet')
        peso_pet = request.POST.get('peso_pet')

        context = self.get_context_data()

        # Verificar se o CPF do condômino existe
        try:
            user_condominio = self.request.user.n_condominio
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino_id, n_condominio=user_condominio)
        except CustomCondomino.DoesNotExist:
            context['form_errors'] = 'Condômino inexistente.'
            return render(request, self.template_name, context)

        # Obter o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        # Criar linha na tabela pets com o n_condominio do usuário logado
        try:
            if condomino_instance and user_condominio_instance:
                CustomPets.objects.create(
                    cpf_condomino=condomino_instance,  # Usar a instância de CustomCondomino
                    nome_pet=nome_pet,
                    raca_pet=raca_pet,
                    altura_pet=altura_pet,
                    peso_pet=peso_pet,
                    n_condominio=user_condominio_instance  # Usar o n_condominio do usuário logado
                )
        except IntegrityError:
            context['form_errors'] = 'Erro ao cadastrar'
            return render(request, self.template_name, context)
        except Exception as e:
            context['form_errors'] = f'Ocorreu erro inesperado: {str(e)}'
            return render(request, self.template_name, context)

        return HttpResponseRedirect(self.success_url)
    



# Tela Alteração Pets
class PetsUpdateViews(View):
    template_name = 'pets/pets_update.html'
    success_url = reverse_lazy("pets_list")

    def get_context_data(self, pk, **kwargs):
        context = {}
        context['pets'] = CustomPets.objects.get(pk=pk)  # Carregar o pet com base no pk
        context['messages'] = messages.get_messages(self.request) 

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(pk=kwargs['pk'])
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        pets = CustomPets.objects.get(pk=pk)

        # Obter o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        # Atualizar os dados com base no formulário
        pets.nome_pet = request.POST.get('nome_pet')
        pets.raca_pet = request.POST.get('raca_pet')
        pets.altura_pet = request.POST.get('altura_pet')
        pets.peso_pet = request.POST.get('peso_pet')
        pets.n_condominio = user_condominio_instance

        try:
            pets.save()  # Salva as alterações no pet

        except Exception as e:
            messages.error(request, 'Erro ao alterar o pet.')
            context = self.get_context_data(pk=pk)
            return render(request, self.template_name, context)

        return redirect(self.success_url)



# Tela Exclusão Pets
class PetsDeleteViews(DeleteView):
    model = CustomPets
    success_url = reverse_lazy("pets_list")
    



#----------------------- SUBSISTEMA FINANCEIRO ....................................................................................................................


#-----------------------Views Plano de Contas.......................................................
        
# Tela Lista Plano Contas 
class FinanceiroEstruturaListViews(LoginRequiredMixin, ListView):
    model = FinanceiroEstrutura
    context_object_name = 'financeiro_estrutura_list'
    
    def get_queryset(self):
        # Get the user's associated condominium
        user_condominio = self.request.user.n_condominio
        # Filter the finance structure based on the user's condominium
        return FinanceiroEstrutura.objects.filter(n_condominio=user_condominio)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        financeiro_estrutura_list = self.get_queryset()
            

        # Função para ordenar com base no nível hierárquico
        def sort_key(fel):
            nivel = fel.get_nivel()
            if nivel:
                return [int(n) for n in nivel.split('.') if n]
            return []

        sorted_list = sorted(financeiro_estrutura_list, key=sort_key)

        # Adicionar padding_left baseado no nível
        for fel in sorted_list:
            nivel = fel.get_nivel()
            if nivel:
                nivel_count = len(nivel.split('.'))
                fel.padding_left = nivel_count * 20  # Ajustar o valor conforme a necessidade
            else:
                fel.padding_left = 0

        context['financeiro_estrutura_list'] = sorted_list
        return context



# Tela Cadastro Plano de contas
@method_decorator(login_required, name='dispatch')
class FinanceiroEstruturaCreateViews(CreateView):
    model = FinanceiroEstrutura
    fields = ['nome', 'parent']
    template_name = 'financeiro_estrutura_form.html'
    success_url = reverse_lazy('financeiro_estrutura_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user_condominio = self.request.user.n_condominio
            # context['categorias'] = FinanceiroEstrutura.objects.filter(n_condominio=user_condominio)
            context['categorias'] = FinanceiroEstrutura.objects.filter(n_condominio=user_condominio).order_by('parent', 'nome')

        except ProgrammingError:
            context['categorias'] = []
           
        return context

    def form_valid(self, form):
       # Atribuir automaticamente o n_condominio do usuário logado 
        form.instance.n_condominio = self.request.user.n_condominio
        
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar a conta.')
        return super().form_invalid(form)
    

    
# Tela altera Plano de contas
class FinanceiroEstruturaUpdateViews(UpdateView):
    model = FinanceiroEstrutura
    context_object_name = 'financeiro_estrutura'
    fields = ['nome']  # Não inclui 'n_condominio' nos campos editáveis
    success_url = reverse_lazy('financeiro_estrutura_list')

    def get_form(self, form_class=None):
        # Obtém o formulário padrão e remove o campo 'n_condominio'
        form = super().get_form(form_class)
        form.fields.pop('n_condominio', None)
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user_condominio = self.request.user.n_condominio
            context['categorias'] = FinanceiroEstrutura.objects.filter(n_condominio=user_condominio)
        except ProgrammingError:
            context['categorias'] = []
            
        return context

    def form_valid(self, form):
        # Atribui o 'n_condominio' do usuário
        form.instance.n_condominio = self.get_object().n_condominio  # Mantém o valor existente
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao alterar a conta.')
        return super().form_invalid(form)
    

    
# Tela Exclusão Plano de contas
class FinanceiroEstruturaDeleteViews(DeleteView):
    model = FinanceiroEstrutura
    success_url = reverse_lazy("financeiro_estrutura_list")
    
    



#-----------------------Views Caixa.................................................................

# Tela Lista Caixa
class CaixaListViews(LoginRequiredMixin, ListView):
    model = Caixa
    context_object_name = 'caixas_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os caixas pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        caixas = Caixa.objects.filter(n_condominio=user_condominio)

        # Adicionar saldo para cada caixa
        for caixa in caixas:
            saldo_instituicao = 0
            try:
                saldo = SaldoCaixaBanco.objects.get(
                    caixa_id=caixa.caixa_id,
                    n_condominio=user_condominio
                )
                saldo_instituicao = saldo.saldo_instituicao  # Adiciona o saldo ao objeto banco
            except SaldoCaixaBanco.DoesNotExist:
                caixa.saldo_instituicao = 0  # Se não encontrado, define como 0 ou outra lógica que você preferir

            # Adicionar saldo ao objeto banco ou ao contexto, dependendo da sua necessidade
            caixa.saldo_instituicao = saldo_instituicao 

        context['caixas_list'] = caixas
        
        return context



# Tela Cadastra Caixa
@method_decorator(login_required, name='dispatch')
class CaixaCreateViews(View):
    template_name = 'caixas/caixas_create.html'
    success_url = reverse_lazy("caixas_list")

    def get_context_data(self, **kwargs):
        context = {}

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs): 
        nome_caixa = request.POST.get('nome_caixa', '')

        context = self.get_context_data()
    
        # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        if user_condominio_instance is None:
            messages.error(self.request, 'Condomínio não associado ao usuário.')
            return render(request, self.template_name, context)
        
                # Validar se o Caixa já está cadastrado
        if Caixa.objects.filter(nome_caixa=nome_caixa, n_condominio=user_condominio_instance).exists():
            messages.error(self.request, 'Caixa já cadastrado.')
            return render(request, self.template_name, context)
        
        # Criar linha na tabela unidade com o n_condominio do usuário logado
        try:
            with transaction.atomic():
                
                # Cria o registro em Caixa
                caixa = Caixa.objects.create(
                    nome_caixa=nome_caixa,
                    n_condominio=user_condominio_instance
                )

                # Cria o registro em SaldoCaixaBanco associado ao Caixa criado
                SaldoCaixaBanco.objects.create(
                    caixa_id=caixa,
                    banco_id=None,
                    saldo_instituicao=0,
                    n_condominio=user_condominio_instance
                )

        except IntegrityError:
            context['form_errors'] = 'Erro ao cadastrar o Caixa .'
            return render(request, self.template_name, context)
        
        except Exception as e:
            context['form_errors'] = f'Ocorreu erro inesperado: {str(e)}'
            return render(request, self.template_name, context)

        return HttpResponseRedirect(self.success_url)  



# Tela Alteração Caixa
class CaixaUpdateViews(UpdateView):
    model = Caixa
    context_object_name = 'caixa'
    fields = [
         "nome_caixa"
    ]
    success_url = reverse_lazy("caixas_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        # Usa get_object para obter o objeto que está sendo atualizado
        Caixa = self.get_object()

        # Obter o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        # Atualizar os dados com base no formulário
        Caixa.nome_caixa = request.POST.get('nome_caixa')
        Caixa.n_condominio = user_condominio_instance

        try:
            Caixa.save()  # Salva as alterações na tabela Banco
        except Exception as e:
            messages.error(request, 'Erro ao alterar o Caixa.')
            return self.form_invalid(caixa)

        return redirect(self.success_url)

    def form_invalid(self, form):
        context = self.get_context_data()
        return render(self.request, self.template_name, context)



# Tela Exclusão Caixa
@method_decorator(login_required, name='dispatch')
class CaixaDeleteViews(View):
    template_name = 'caixas/caixa_delete.html'
    success_url = reverse_lazy("caixas_list")

    def get(self, request, *args, **kwargs):
        # Renderiza a página de confirmação de exclusão
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Obtém o ID do Caixa a ser excluído
        caixa_id = kwargs.get('pk')  # ou a lógica que você usa para obter o ID
        user_condominio_instance = request.user.n_condominio
        try:
            with transaction.atomic():
                # Obtém a instância do Caixa a ser excluído
                caixa = Caixa.objects.get(caixa_id=caixa_id)

                # Exclui as linhas correspondentes na tabela SaldoCaixaBanco
                SaldoCaixaBanco.objects.filter(
                    caixa_id=caixa.caixa_id,
                    n_condominio=user_condominio_instance
                ).delete()

                # Exclui a linha na tabela Caixa
                caixa.delete()
                
                messages.success(request, 'Caixa excluído com sucesso!')
        except Caixa.DoesNotExist:
            messages.error(request, 'Caixa não encontrado.')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro: {str(e)}')

        return HttpResponseRedirect(self.success_url)



#-----------------------Views Bancos.................................................................

# Tela Lista Banco
class BancoListViews(LoginRequiredMixin, ListView):
    model = Banco
    context_object_name = 'bancos_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os bancos pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        bancos = Banco.objects.filter(n_condominio=user_condominio)

        # Adicionar saldo para cada banco
        for banco in bancos:
            saldo_instituicao = 0  # Inicializa a variável antes do try
            try:
                saldo = SaldoCaixaBanco.objects.get(
                    banco_id=banco.banco_id,
                    n_condominio=user_condominio
                )
                saldo_instituicao = saldo.saldo_instituicao  # Adiciona o saldo ao objeto banco
            except SaldoCaixaBanco.DoesNotExist:
                messages.error('Saldo não encontrado para o banco.')
                
            # Adicionar saldo ao objeto banco ou ao contexto, dependendo da sua necessidade
            banco.saldo_instituicao = saldo_instituicao  # Pode criar um atributo dinamicamente se necessário

        context['bancos_list'] = bancos
        
        return context

    



# Tela Cadastra Banco
@method_decorator(login_required, name='dispatch')
class BancoCreateViews(View):
    template_name = 'bancos/bancos_create.html'
    success_url = reverse_lazy("bancos_list")

    def get_context_data(self, **kwargs):
        context = {}

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs): 
        n_banco = request.POST.get('n_banco', '')
        agencia = request.POST.get('agencia', '')
        conta_corrente = request.POST.get('conta_corrente', '')
        nome_banco = request.POST.get('nome_banco', '')
        telefone = request.POST.get('telefone', '')
        celular = request.POST.get('celular', '')
        email = request.POST.get('email', '')

        context = self.get_context_data()
    
        # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        if user_condominio_instance is None:
            messages.error(self.request, 'Condomínio não associado ao usuário.')
            return render(request, self.template_name, context)

        # Validar se o Banco já está cadastrado
        if Banco.objects.filter(n_banco=n_banco, agencia=agencia, conta_corrente=conta_corrente, n_condominio=user_condominio_instance).exists():
            messages.error(self.request, 'Banco já cadastrado.')
            return render(request, self.template_name, context)
        
        # Criar linha na tabela unidade com o n_condominio do usuário logado
        try:
            with transaction.atomic():
                # Cria o registro em Banco
                banco = Banco.objects.create(
                    n_banco=n_banco,
                    agencia=agencia,
                    conta_corrente=conta_corrente,
                    nome_banco=nome_banco,
                    telefone=telefone,
                    celular=celular,
                    email=email,
                    n_condominio=user_condominio_instance
                )
                # Cria o registro em SaldoCaixaBanco associado ao Banco criado
                SaldoCaixaBanco.objects.create(
                    caixa_id=None,
                    banco_id=banco,
                    saldo_instituicao=0,
                    n_condominio=user_condominio_instance
                )          
        except IntegrityError:
            context['form_errors'] = 'Erro ao cadastrar o Banco/Saldo inicial.'
            return render(request, self.template_name, context)

        except Exception as e:
            context['form_errors'] = f'Ocorreu erro inesperado: {str(e)}'
            return render(request, self.template_name, context)
  
        return HttpResponseRedirect(self.success_url)  



# Tela Alteração Banco
class BancoUpdateViews(UpdateView):
    model = Banco
    context_object_name = 'banco'
    fields = [
        "n_banco", "agencia", "conta_corrente", "nome_banco", "telefone", "celular", "email"
    ]
    success_url = reverse_lazy("bancos_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'banco' já está disponível no contexto como self.object
        # context['bancos_list'] = Banco.objects.all()  # Se você quiser a lista de todos os bancos
        return context

    def post(self, request, *args, **kwargs):
        # Usa get_object para obter o objeto que está sendo atualizado
        banco = self.get_object()

        # Obter o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        # Atualizar os dados com base no formulário
        banco.n_banco = request.POST.get('n_banco')
        banco.agencia = request.POST.get('agencia')
        banco.conta_corrente = request.POST.get('conta_corrente')
        banco.nome_banco = request.POST.get('nome_banco')
        banco.telefone = request.POST.get('telefone')
        banco.celular = request.POST.get('celular')
        banco.email = request.POST.get('email')
        banco.n_condominio = user_condominio_instance

        try:
            banco.save()  # Salva as alterações na tabela Banco
        except Exception as e:
            messages.error(request, 'Erro ao alterar o Banco.')
            return self.form_invalid(banco)

        return redirect(self.success_url)

    def form_invalid(self, form):
        context = self.get_context_data()
        return render(self.request, self.template_name, context)



# Tela Exclusão de Banco
@method_decorator(login_required, name='dispatch')
class BancoDeleteViews(View):
    template_name = 'bancos/banco_delete.html'
    success_url = reverse_lazy("bancos_list")

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        banco_id = kwargs.get('pk')
        try:
            with transaction.atomic():
                banco = Banco.objects.get(pk=banco_id)
                user_condominio_instance = request.user.n_condominio
                # Exclui a linha correspondente na tabela SaldoCaixaBanco com base nos valores de Banco
                SaldoCaixaBanco.objects.filter(
                    banco_id=banco.banco_id,
                    n_condominio=user_condominio_instance
                ).delete()

                # Exclui a linha correspondente na tabela banco
                banco.delete()
                
                messages.success(request, 'Banco excluído com sucesso!')
        except Banco.DoesNotExist:
            messages.error(request, 'Banco não encontrado.')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro: {str(e)}')

        return HttpResponseRedirect(self.success_url)



#-----------------------Views Fornecedores.................................................................

# Tela Lista os Fornecedores 
class FornecedoresListViews(LoginRequiredMixin, ListView):
    model = Fornecedor
    context_object_name = 'fornecedores_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar as mudanças pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['fornecedores_list'] = Fornecedor.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastro de Fornecedores
@method_decorator(login_required, name='dispatch')
class FornecedoresCreateViews(View):
    template_name = 'fornecedores/fornecedores_create.html'
    success_url = reverse_lazy("fornecedores_list")

    def get_context_data(self, **kwargs):
        context = {}        
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):    
        cnpj = request.POST.get('cnpj')
        razaoSocial = request.POST.get('razaoSocial')
        nomeFantasia = request.POST.get('nomeFantasia')
        cpf_fornecedor = request.POST.get('cpf_fornecedor')
        endereco = request.POST.get('endereco')
        telefone = request.POST.get('telefone')
        celular = request.POST.get('celular')
        email = request.POST.get('email')

        context = self.get_context_data()
        
        # Verifica se o CNPJ e CPF já estão cadastrados
        if Fornecedor.objects.filter(cnpj=cnpj, cpf_fornecedor=cpf_fornecedor).exists():
            messages.error(request, 'CNPJ já cadastrado com este CPF.')
            return render(request, self.template_name, context)
        
        # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        try:
            condomino_instance = CustomCondomino.objects.get(n_condominio=user_condominio_instance)
            if condomino_instance and user_condominio_instance:
                Fornecedor.objects.create(
                    cnpj=cnpj,  
                    razaoSocial=razaoSocial,
                    nomeFantasia=nomeFantasia,
                    cpf_fornecedor=cpf_fornecedor,
                    endereco=endereco,
                    telefone=telefone,
                    celular=celular,
                    email=email,
                    n_condominio=user_condominio_instance  # Usa o n_condominio do usuário logado
                )
        except IntegrityError:
            messages.error(request, 'Erro ao cadastrar o fornecedor.')
            # context['form_errors'] = 'Erro ao cadastrar'
            return render(request, self.template_name, context)
        except Exception as e:
            messages.error(request, f'Ocorreu um erro inesperado: {e}')
            return render(request, self.template_name, context)

        return HttpResponseRedirect(self.success_url)



# Tela Alteração de Fornecedores
class FornecedoresUpdateViews(UpdateView):
    model = Fornecedor
    template_name = 'fornecedores/fornecedores_update.html'
    context_object_name = 'fornecedor'
    fields = [
        "cnpj", "razaoSocial", "nomeFantasia", "cpf_fornecedor", "endereco", "telefone", "celular", "email"
    ]
    success_url = reverse_lazy("fornecedores_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fornecedor'] = self.get_object()  # Certifique-se de passar o objeto fornecedor no contexto
        return context

    def post(self, request, *args, **kwargs):
        # Recupera o objeto fornecedor usando get_object()
        self.object = self.get_object()

        cnpj = request.POST.get('cnpj')
        razaoSocial = request.POST.get('razaoSocial')
        nomeFantasia = request.POST.get('nomeFantasia')
        cpf_fornecedor = request.POST.get('cpf_fornecedor')
        endereco = request.POST.get('endereco')
        telefone = request.POST.get('telefone')
        celular = request.POST.get('celular')
        email = request.POST.get('email')

        context = self.get_context_data()

        # Verifica se o CNPJ e CPF já estão cadastrados
        if Fornecedor.objects.filter(cnpj=cnpj, cpf_fornecedor=cpf_fornecedor).exclude(pk=self.object.pk).exists():
            messages.error(request, 'CNPJ já cadastrado com este CPF.')
            return render(request, self.template_name, context)

        # Atualiza os campos do fornecedor
        self.object.cnpj = cnpj
        self.object.razaoSocial = razaoSocial
        self.object.nomeFantasia = nomeFantasia
        self.object.cpf_fornecedor = cpf_fornecedor
        self.object.endereco = endereco
        self.object.telefone = telefone
        self.object.celular = celular
        self.object.email = email
        self.object.n_condominio = request.user.n_condominio  # Usa o condomínio do usuário logado

        try:
            self.object.save()  # Salva a instância modificada
        except Exception as e:
            messages.error(request, f'Erro ao alterar o fornecedor: {e}')
            return render(request, self.template_name, context)

        return redirect(self.success_url)

 



# Tela Exclusão de Fornecedores
class FornecedoresDeleteViews(DeleteView):
    model = Fornecedor
    success_url = reverse_lazy("fornecedores_list")



#-----------------------Views Contas a Receber.................................................................

# Tela Lista Contas a Receber
class ContasReceberListViews(LoginRequiredMixin, ListView):
    model = ContaReceber
    context_object_name = 'contas_receber_list'    

    def get_context_data(self, **kwargs): 
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar as contas a receber pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['contas_receber_list'] = ContaReceber.objects.filter(
            n_condominio=user_condominio, data_recebimento__isnull=True  
        )
        
        return context



# Tela Cadastra Contas a Receber 
@method_decorator(login_required, name='dispatch')
class ContasReceberCreateViews(CreateView):
    model = ContaReceber
    fields = [
        "categoria", "unidade_id", "tipo_documento", "numero_documento", "data_vencimento", "valor"
    ]
    success_url = reverse_lazy("contas_receber_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_condominio = self.request.user.n_condominio
        context['categorias'] = [categoria for categoria in FinanceiroEstrutura.objects.filter(n_condominio=user_condominio) if len(categoria.get_nivel().split('.')) >= 3 and categoria.get_nivel() <= '2' ]
        context['unidades'] = CustomUnidade.objects.filter(n_condominio=user_condominio)

        return context

    def form_valid(self, form):
        # Atribuir o n_condominio com base no usuário logado
        form.instance.n_condominio = self.request.user.n_condominio

        # Remover caracteres especiais da data, se necessário
        data_vencimento_formatada = form.cleaned_data.get('data_vencimento').strftime('%Y%m%d')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao cadastrar a conta.')
        
        return super().form_invalid(form)



# Tela Altera Contas a Receber 
class ContasReceberUpdateViews(UpdateView):
    model = ContaReceber
    fields = [
        "categoria", "unidade_id", "tipo_documento", "numero_documento", "data_vencimento", "valor"   
    ]
    success_url = reverse_lazy("contas_receber_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Customize the widget for 'data_orcamento_despesa' to be a text input for 'mm-yyyy'
        form.fields['data_orcamento_despesa'].widget = forms.TextInput(attrs={
            'id': 'data_orcamento_despesa',
            'class': 'form-control-sm',
            'placeholder': 'mm-yyyy',
            'required': 'required'
        })
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_condominio = self.request.user.n_condominio
        context['categorias'] = [categoria for categoria in FinanceiroEstrutura.objects.filter(n_condominio=user_condominio) if len(categoria.get_nivel().split('.')) >= 3 and categoria.get_nivel() <= '2' ]
        context['unidades'] = CustomUnidade.objects.filter(n_condominio=user_condominio)

        # Passa o ID da unidade atual ao contexto
        context['unidade_atual_id'] = self.object.unidade_id_id  # Usa unidade_id_id para obter o ID direto

        return context

    def form_valid(self, form):
        form.instance.n_condominio = self.request.user.n_condominio
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao alterar a conta.')
        return self.render_to_response(self.get_context_data(form=form))



# Tela Exclusão Contas a Receber
class ContasReceberDeleteViews(DeleteView):
    model = ContaReceber
    success_url = reverse_lazy("contas_receber_list")
    
    


# Tela Cadastra Recebimento no Contas a Receber e no SaldoCaixaBanco  
class ContasReceberReceber(View):
    template_name = 'contas_receber/contas_receber_receber.html'
    success_url = reverse_lazy("contas_receber_list")

    def get_context_data(self, pk, **kwargs):
        context = {}
        user_condominio = self.request.user.n_condominio        
        context['bancos'] = Banco.objects.filter(n_condominio=user_condominio)
        context['caixas'] = Caixa.objects.filter(n_condominio=user_condominio)

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(pk=kwargs['pk'])
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        conta_receber = ContaReceber.objects.get(pk=pk)
        user_condominio_instance = request.user.n_condominio


        # Obter o valor do select 'bancoCaixa' (unidade_id)
        banco_caixa_id = request.POST.get('bancoCaixa')
        data_recebimento = request.POST.get('data_recebimento')
        valor_recebido = Decimal(request.POST.get('valor_recebido').replace(',', '.'))        

        # Inicializa as variáveis caixa e banco com None
        caixa = None
        banco = None

        try:
            with transaction.atomic():

                if banco_caixa_id.startswith('caixa_'):
                    caixa_id = banco_caixa_id.split('_')[1]  # Extrai o ID do caixa
                    caixa = Caixa.objects.filter(caixa_id=caixa_id, n_condominio=user_condominio_instance).first()
                    banco = None  # Nenhum banco foi selecionado

                elif banco_caixa_id.startswith('banco_'):
                    banco_id = banco_caixa_id.split('_')[1]  # Extrai o ID do banco
                    banco = Banco.objects.filter(banco_id=banco_id, n_condominio=user_condominio_instance).first()
                    caixa = None  # Nenhum caixa foi selecionado

                else:
                    caixa = None
                    banco = None

                conta_receber.data_recebimento = data_recebimento
                conta_receber.valor_recebido = valor_recebido
                conta_receber.caixa_id=caixa
                conta_receber.banco_id=banco
                conta_receber.n_condominio = user_condominio_instance
                conta_receber.save()

                # Atualiza o saldo em SaldoCaixaBanco para o banco ou caixa selecionado
                if banco:
                    saldo_banco = SaldoCaixaBanco.objects.get(banco_id=banco.banco_id, n_condominio=user_condominio_instance)
                    saldo_banco.saldo_instituicao += valor_recebido
                    saldo_banco.save()
                elif caixa:
                    saldo_caixa = SaldoCaixaBanco.objects.get(caixa_id=caixa.caixa_id, n_condominio=user_condominio_instance)
                    saldo_caixa.saldo_instituicao += valor_recebido
                    saldo_caixa.save()

        except IntegrityError:
            context = self.get_context_data(pk=kwargs['pk'])
            context['form_errors'] = 'Erro ao cadastrar o recebimento.'
            return render(request, self.template_name, context)

        except Exception as e:
            context = self.get_context_data(pk=kwargs['pk'])
            context['form_errors'] = f'Ocorreu um erro inesperado: {str(e)}'
            return render(request, self.template_name, context)

        return HttpResponseRedirect(self.success_url)



#-----------------------Views Contas a Pagar.................................................................

# Tela Lista Contas a Pagar
class ContasPagarListViews(LoginRequiredMixin, ListView):
    model = ContaPagar
    context_object_name = 'contas_pagar_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar as contas a pagar pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio        
        context['contas_pagar_list'] = ContaPagar.objects.filter(
            n_condominio=user_condominio, data_pagamento__isnull=True  
        )


        return context



# Tela Cadastra Contas a Pagar
@method_decorator(login_required, name='dispatch')
class ContasPagarCreateViews(View):
    template_name = 'contas_pagar/contas_pagar_create.html'    
    success_url = reverse_lazy("contas_pagar_list")

    def get_context_data(self, **kwargs):
        context = {}
        user_condominio = self.request.user.n_condominio
        context['categorias'] = [
            categoria for categoria in FinanceiroEstrutura.objects.filter(n_condominio=user_condominio) 
            if len(categoria.get_nivel().split('.')) >= 3 and categoria.get_nivel() >= '2'
        ]
        context['fornecedores'] = Fornecedor.objects.filter(n_condominio=user_condominio)
        context['tipo_documento'] = [
            ('Nota fiscal', 'Nota Fiscal'),
            ('Recibo', 'Recibo'),
            ('Boleto', 'Boleto')
        ]
        context['messages'] = messages.get_messages(self.request)  # Adicione esta linha p aparecer a mensagem
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):    
        categoria_id = request.POST.get('categoria')  # Obtenha o ID da categoria
        fornecedor_id = request.POST.get('fornecedor_id')  # Obtenha o ID do fornecedor
        tipo_documento = request.POST.get('tipo_documento')
        numero_documento = request.POST.get('numero_documento')
        documento = request.FILES.get('documento') 
        data_vencimento_str = request.POST.get('data_vencimento')
        valor = Decimal(request.POST.get('valor').replace(',', '.'))    

        context = self.get_context_data()  # Use o método aqui

        # Verifica se já existe um documento cadastrado
        if ContaPagar.objects.filter(fornecedor_id=fornecedor_id, numero_documento=numero_documento, data_vencimento=data_vencimento_str).exists():
            messages.error(request, 'Documento já cadastrado.')
            return render(request, self.template_name, context)

        if not documento:
            messages.error(request, 'O campo Documento é obrigatório.')
            return render(request, self.template_name, context)

        # Obtém o n_condominio do usuário logado
        user_condominio_instance = request.user.n_condominio

        try:
            # Obtém a instância da categoria
            categoria_instance = get_object_or_404(FinanceiroEstrutura, pk=categoria_id)

            # Obtém a instância do fornecedor
            fornecedor_instance = get_object_or_404(Fornecedor, pk=fornecedor_id)

            conta_pagar = ContaPagar.objects.create(
                categoria=categoria_instance,  # Atribua a instância da categoria
                fornecedor_id=fornecedor_instance,  # Atribua a instância do fornecedor
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                documento=documento,
                data_vencimento=data_vencimento_str,  # Certifique-se de que está no formato correto
                valor=valor,
                n_condominio=user_condominio_instance  # Usa o n_condominio do usuário logado
            )                
            conta_pagar.save()

        except IntegrityError as e:
            messages.error(request, f'Erro de integridade: {e}')
            return render(request, self.template_name, context)
        except ValidationError as e:
            messages.error(request, f'Erro de validação: {e}')
            return render(request, self.template_name, context)
        except Exception as e:
            messages.error(request, f'Ocorreu um erro inesperado: {e}')
            return render(request, self.template_name, context)

        return redirect(self.success_url)
    



# Tela Alteração Contas a Pagar
class ContasPagarUpdateViews(UpdateView):
    model = ContaPagar
    fields = [
        "categoria", "fornecedor_id", "tipo_documento",
        "numero_documento", "documento", "data_vencimento", "valor"
    ]
    success_url = reverse_lazy("contas_pagar_list")

    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Atualiza as escolhas do campo tipo_documento para garantir que estão corretas
        form.fields['tipo_documento'].choices = [
            ('Nota fiscal', 'Nota fiscal'),
            ('Recibo', 'Recibo'),
            ('Boleto', 'Boleto')
        ]
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_condominio = self.request.user.n_condominio
        context['categorias'] = [
            categoria for categoria in FinanceiroEstrutura.objects.filter(n_condominio=user_condominio)
            if len(categoria.get_nivel().split('.')) >= 3 and categoria.get_nivel() >= '2'
        ]
        context['fornecedores'] = Fornecedor.objects.filter(n_condominio=user_condominio)
        context['tipo_documento'] = [
            ('Nota fiscal', 'Nota fiscal'),
            ('Recibo', 'Recibo'),
            ('Boleto', 'Boleto')
        ]
        context['fornecedor_atual_id'] = self.object.fornecedor_id_id
        context['messages'] = messages.get_messages(self.request)

        # Inicializa o tipo de documento corretamente se estiver faltando
        if 'form' in kwargs:
            kwargs['form'].fields['tipo_documento'].choices = context['tipo_documento']

        return context

    def form_valid(self, form):
        # Validações antes de salvar
        categoria_id = self.request.POST.get('categoria')
        fornecedor_id = self.request.POST.get('fornecedor_id')
        tipo_documento = self.request.POST.get('tipo_documento')
        numero_documento = self.request.POST.get('numero_documento')
        documento = self.request.FILES.get('documento')
        data_vencimento_str = self.request.POST.get('data_vencimento')
        valor = Decimal(self.request.POST.get('valor').replace(',', '.'))

        # Verifica se já existe um documento cadastrado com os mesmos dados
        if ContaPagar.objects.filter(
            fornecedor_id=fornecedor_id,
            numero_documento=numero_documento,
            data_vencimento=data_vencimento_str
        ).exclude(pk=self.object.pk).exists():
            messages.error(self.request, 'Documento já cadastrado.')
            return self.form_invalid(form)

        if not documento:
            # Atualiza os campos no objeto sem substituição do 'documento'.
            try:
                categoria_instance = get_object_or_404(FinanceiroEstrutura, pk=categoria_id)
                fornecedor_instance = get_object_or_404(Fornecedor, pk=fornecedor_id)
                self.object.categoria = categoria_instance
                self.object.fornecedor_id = fornecedor_instance
                self.object.tipo_documento = tipo_documento
                self.object.numero_documento = numero_documento
                self.object.data_vencimento = data_vencimento_str
                self.object.valor = valor
                self.object.n_condominio = self.request.user.n_condominio

                return super().form_valid(form)

            except (IntegrityError, ValidationError) as e:
                messages.error(self.request, f'Erro ao salvar: {e}')
                return self.form_invalid(form)

            except Exception as e:
                messages.error(self.request, f'Ocorreu um erro inesperado: {e}')
                return self.form_invalid(form)
        else:
            # Atualiza os campos no objeto com substituição do 'documento'.
            try:
                categoria_instance = get_object_or_404(FinanceiroEstrutura, pk=categoria_id)
                fornecedor_instance = get_object_or_404(Fornecedor, pk=fornecedor_id)
                self.object.categoria = categoria_instance
                self.object.fornecedor_id = fornecedor_instance
                self.object.tipo_documento = tipo_documento
                self.object.numero_documento = numero_documento
                self.object.documento = documento
                self.object.data_vencimento = data_vencimento_str
                self.object.valor = valor
                self.object.n_condominio = self.request.user.n_condominio

                return super().form_valid(form)

            except (IntegrityError, ValidationError) as e:
                messages.error(self.request, f'Erro ao salvar: {e}')
                return self.form_invalid(form)

            except Exception as e:
                messages.error(self.request, f'Ocorreu um erro inesperado: {e}')
                return self.form_invalid(form)


    def form_invalid(self, form):

        return self.render_to_response(self.get_context_data(form=form))

   



# Tela Exclusão Contas a Pagar
class ContasPagarDeleteViews(DeleteView):
    model = ContaPagar
    success_url = reverse_lazy("contas_pagar_list")
   
    


# Tela Cadastra Pagamento no Contas a Pagar e no SaldoCaixaBanco  
class ContasPagarPagar(View):
    template_name = 'contas_pagar/contas_pagar_pagar.html'
    success_url = reverse_lazy("contas_pagar_list")

    def get_context_data(self, pk, **kwargs):
        context = {}
        context['pk'] = pk
        user_condominio = self.request.user.n_condominio        
        context['bancos'] = Banco.objects.filter(n_condominio=user_condominio)
        context['caixas'] = Caixa.objects.filter(n_condominio=user_condominio)

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(pk=kwargs['pk'])
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        conta_pagar = ContaPagar.objects.get(pk=pk)
        user_condominio_instance = request.user.n_condominio

        # Obter o valor do select 'bancoCaixa' (unidade_id)
        banco_caixa_id = request.POST.get('bancoCaixa')
        data_pagamento = request.POST.get('data_pagamento')
        valor_pago = Decimal(request.POST.get('valor_pago').replace(',', '.'))
        
        # Inicializa as variáveis caixa e banco com None
        caixa = None
        banco = None

        try:
            with transaction.atomic():

                if banco_caixa_id.startswith('caixa_'):
                    caixa_id = banco_caixa_id.split('_')[1]  # Extrai o ID do caixa
                    
                    # Obtém o saldo da instituição na tabela SaldoCaixaBanco
                    saldo_instituicao = SaldoCaixaBanco.objects.filter(caixa_id=caixa_id, n_condominio=user_condominio_instance).values_list('saldo_instituicao', flat=True).first()
                    
                    if saldo_instituicao is not None and saldo_instituicao < valor_pago:
                        mensagem = "Saldo de Caixa insuficiente para o pagamento."
                        messages.error(request, mensagem)  # Adiciona a mensagem de erro
                        return render(request, 'contas_pagar/contas_pagar_pagar.html', {'banco_caixa_id': banco_caixa_id, 'valor_pago': valor_pago})
                    
                    else:
                        caixa = Caixa.objects.filter(caixa_id=caixa_id, n_condominio=user_condominio_instance).first()
                        banco = None  # Nenhum banco foi selecionado

                elif banco_caixa_id.startswith('banco_'):
                    banco_id = banco_caixa_id.split('_')[1]  # Extrai o ID do banco
                    
                    # Obtém o saldo da instituição na tabela SaldoCaixaBanco
                    saldo_instituicao = SaldoCaixaBanco.objects.filter(banco_id=banco_id, n_condominio=user_condominio_instance).values_list('saldo_instituicao', flat=True).first()
                    
                    if saldo_instituicao is not None and saldo_instituicao < valor_pago:
                        mensagem = "Saldo do Banco insuficiente para o pagamento."
                        messages.error(request, mensagem)  # Adiciona a mensagem de erro
                        return render(request, 'contas_pagar/contas_pagar_pagar.html', {'banco_caixa_id': banco_caixa_id, 'valor_pago': valor_pago})
                    
                    else:
                        banco = Banco.objects.filter(banco_id=banco_id, n_condominio=user_condominio_instance).first()
                        caixa = None  # Nenhum caixa foi selecionado

                else:
                    caixa = None
                    banco = None
           
                conta_pagar.data_pagamento = data_pagamento
                conta_pagar.valor_pago = valor_pago
                conta_pagar.caixa_id=caixa
                conta_pagar.banco_id=banco
                conta_pagar.n_condominio = user_condominio_instance
                conta_pagar.save()

                # Atualiza o saldo em SaldoCaixaBanco para o banco ou caixa selecionado
                if banco:
                    saldo_banco = SaldoCaixaBanco.objects.get(banco_id=banco.banco_id, n_condominio=user_condominio_instance)
                    saldo_banco.saldo_instituicao -= valor_pago
                    saldo_banco.save()
                elif caixa:
                    saldo_caixa = SaldoCaixaBanco.objects.get(caixa_id=caixa.caixa_id, n_condominio=user_condominio_instance)
                    saldo_caixa.saldo_instituicao -= valor_pago
                    saldo_caixa.save()

        except IntegrityError:
            context = self.get_context_data(pk=kwargs['pk'])
            messages.error(self.request, 'Erro ao cadastrar o pagamento.')
            return render(request, self.template_name, context)

        except Exception as e:
            context = self.get_context_data(pk=kwargs['pk'])
            return render(request, self.template_name, context)

        return HttpResponseRedirect(self.success_url)



# -----------------------Views Previsao Receitas.................................................................

# Tela Lista Previsao Receitas
class PrevisaoReceitasListViews(LoginRequiredMixin, ListView):
    model = PrevisaoReceitas
    context_object_name = 'previsao_receitas_list'

    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)

        # Filtrar as contas a pagar pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['previsao_receitas_list'] = PrevisaoReceitas.objects.filter(n_condominio=user_condominio)

        return context



# Tela Cadastra Previsao Receitas
@method_decorator(login_required, name='dispatch')
class PrevisaoReceitasCreateViews(CreateView):
    model = PrevisaoReceitas
    fields = ["categoria", "data_orcamento_receita", "valor_orcamento_receita"]
    success_url = reverse_lazy("previsao_receitas_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Set the widget for the data_orcamento_receita field to text for the date picker
        form.fields['data_orcamento_receita'].widget = forms.TextInput(attrs={
            'id': 'data_orcamento_receita',  # Ensure this matches your HTML
            'class': 'form-control-sm',
            'placeholder': 'mm-yyyy',  # Adjust as needed
            'required': 'required'
        })
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_condominio = self.request.user.n_condominio
        context['categorias'] = [
            categoria for categoria in FinanceiroEstrutura.objects.filter(n_condominio=user_condominio) 
            if len(categoria.get_nivel().split('.')) >= 3 and categoria.get_nivel() < '2'
        ]
        context['messages'] = messages.get_messages(self.request)

        return context
    
    def form_valid(self, form):
        # Atribui o n_condominio ao form.instance antes de salvar
        form.instance.n_condominio = self.request.user.n_condominio

        # Obter dados do formulário
        categoria = form.cleaned_data["categoria"]
        valor_orcamento_receita = form.cleaned_data["valor_orcamento_receita"]
        data_inicial = form.cleaned_data["data_orcamento_receita"]

        # Obter valor do checkbox diretamente do POST
        multiplas_entradas = self.request.POST.get("multiplas_entradas", "off") == "on"

        # Verifica se o usuário está autenticado e possui um condomínio associado
        if not self.request.user.is_authenticated or not form.instance.n_condominio:
            form.add_error(None, "Usuário não autenticado ou condomínio não associado.")
            return self.form_invalid(form)

        # Verifica o ano e o mês selecionado
        ano_selecionado = data_inicial.year
        mes_inicial = data_inicial.month

        # Criação das entradas
        if multiplas_entradas:
            
            # Loop para criar entradas mensais até dezembro
            for mes in range(mes_inicial, 13):  # De 'mes_inicial' até dezembro
                data_orcamento = datetime(ano_selecionado, mes, 1).date()

                # Criar instância de 'PrevisaoReceitas' para o mês
                PrevisaoReceitas.objects.create(
                    n_condominio=form.instance.n_condominio,  
                    categoria=categoria,
                    data_orcamento_receita=data_orcamento,
                    valor_orcamento_receita=valor_orcamento_receita,
                )
            
            # Retorna um redirecionamento sem chamar form_valid novamente
            return HttpResponseRedirect(self.success_url)
        else:
            # Cria uma única entrada fora do loop
            return super().form_valid(form)

    def form_invalid(self, form):        
        messages.error(self.request, 'Erro ao cadastrar a previsão de receita.')

        return super().form_invalid(form)



# Tela Alteração Previsao Receitas
class PrevisaoReceitasUpdateViews(UpdateView):
    model = PrevisaoReceitas
    fields = ["valor_orcamento_receita"]  # Apenas o campo a ser atualizado
    context_object_name = 'previsao_receitas_list'
    success_url = reverse_lazy("previsao_receitas_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_orcamento_receita = self.object.data_orcamento_receita

        if data_orcamento_receita:
            ano = data_orcamento_receita.year
            mes = data_orcamento_receita.month
            nomes_meses = {
                1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
                5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
                9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
            }
            mes_nome = nomes_meses.get(mes, "Mês inválido")
            context["ano_orcamento"] = ano
            context["mes_orcamento"] = mes_nome

        user_condominio = self.request.user.n_condominio
        context['categorias'] = [
            categoria for categoria in FinanceiroEstrutura.objects.filter(n_condominio=user_condominio) 
            if len(categoria.get_nivel().split('.')) >= 3 and categoria.get_nivel() < '2'
        ]
        context['messages'] = messages.get_messages(self.request)
        return context

    def form_valid(self, form):

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao alterar a previsão de receita.')

        return super().form_invalid(form)



# Tela Exclusão Previsao Receitas
class PrevisaoReceitasDeleteViews(DeleteView):
    model = PrevisaoReceitas
    success_url = reverse_lazy("previsao_receitas_list")



# -----------------------Views Previsao Despesas.................................................................

# Tela Lista Previsao Despesas
class PrevisaoDespesasListViews(LoginRequiredMixin, ListView):
    model = PrevisaoDespesas
    context_object_name = 'previsao_despesas_list'

    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)

        # Filtrar as contas a pagar pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['previsao_despesas_list'] = PrevisaoDespesas.objects.filter(n_condominio=user_condominio)

        return context



# Tela Cadastra Previsao Despesas
@method_decorator(login_required, name='dispatch')
class PrevisaoDespesasCreateViews(CreateView):
    model = PrevisaoDespesas
    fields = ["categoria", "data_orcamento_despesa", "valor_orcamento_despesa"]
    success_url = reverse_lazy("previsao_despesas_list")

    def get_context_data(self, **kwargs):
        print('Entrei context.......................')
        context = super().get_context_data(**kwargs)
        user_condominio = self.request.user.n_condominio
        context['categorias'] = [
            categoria for categoria in FinanceiroEstrutura.objects.filter(n_condominio=user_condominio) 
            if len(categoria.get_nivel().split('.')) >= 3 and categoria.get_nivel() >= '2'
        ]
        context['messages'] = messages.get_messages(self.request)
        print(f'Context categories: {context["categorias"]}')
        return context
    
    def form_valid(self, form):
        print('Entrou em form_valid')
        form.instance.n_condominio = self.request.user.n_condominio

        # Obter dados do formulário
        categoria = form.cleaned_data["categoria"]
        valor_orcamento_despesa = form.cleaned_data["valor_orcamento_despesa"]
        data_inicial = form.cleaned_data["data_orcamento_despesa"]

        print(f'Dados do formulário - Categoria: {categoria}, Valor: {valor_orcamento_despesa}, Data Inicial: {data_inicial}')

        # Obter valor do checkbox diretamente do POST
        multiplas_entradas = self.request.POST.get("multiplas_entradas", "off") == "on"
        print(f'Multiplas entradas: {multiplas_entradas}')

        if not self.request.user.is_authenticated or not form.instance.n_condominio:
            form.add_error(None, "Usuário não autenticado ou condomínio não associado.")
            print('Erro: Usuário não autenticado ou condomínio não associado')
            return self.form_invalid(form)

        # Verifica o ano e o mês selecionado
        ano_selecionado = data_inicial.year
        mes_inicial = data_inicial.month
        print(f'Ano Selecionado: {ano_selecionado}, Mês Inicial: {mes_inicial}')

        if multiplas_entradas:
            for mes in range(mes_inicial, 13):
                data_orcamento = datetime(ano_selecionado, mes, 1).date()
                print(f'Criando entrada para o mês: {mes}, Data Orcamento: {data_orcamento}')
                try:
                    PrevisaoDespesas.objects.create(
                        n_condominio=form.instance.n_condominio,  
                        categoria=categoria,
                        data_orcamento_despesa=data_orcamento,
                        valor_orcamento_despesa=valor_orcamento_despesa,
                    )
                    print(f'Linha criada com sucesso para o mês {mes}')
                except Exception as e:
                    print(f'Erro ao criar linha para o mês {mes}: {e}')
                    messages.error(self.request, f'Erro ao criar linha para o mês {mes}')
            
            return HttpResponseRedirect(self.success_url)
        else:
            print('Criando uma única entrada fora do loop')
            return super().form_valid(form)

    def form_invalid(self, form):        
        # Mostra quais erros específicos estão ocorrendo no formulário
        print('Entrou em form_invalid')
        for field, errors in form.errors.items():
            print(f'Erro no campo "{field}": {errors}')
        messages.error(self.request, 'Erro ao cadastrar a previsão de despesa.')
        return super().form_invalid(form)



# Tela Alteração Previsao Despesas
class PrevisaoDespesasUpdateViews(UpdateView):
    model = PrevisaoDespesas
    fields = ["valor_orcamento_despesa"]  # Apenas o campo a ser atualizado
    context_object_name = 'previsao_despesas_list'
    success_url = reverse_lazy("previsao_despesas_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_orcamento_despesa = self.object.data_orcamento_despesa

        if data_orcamento_despesa:
            ano = data_orcamento_despesa.year
            mes = data_orcamento_despesa.month
            nomes_meses = {
                1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
                5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
                9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
            }
            mes_nome = nomes_meses.get(mes, "Mês inválido")
            context["ano_orcamento"] = ano
            context["mes_orcamento"] = mes_nome

        user_condominio = self.request.user.n_condominio
        context['categorias'] = [
            categoria for categoria in FinanceiroEstrutura.objects.filter(n_condominio=user_condominio) 
            if len(categoria.get_nivel().split('.')) >= 3 and categoria.get_nivel() < '2'
        ]
        context['messages'] = messages.get_messages(self.request)
        return context

    def form_valid(self, form):

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao alterar a previsão de despesa.')

        return super().form_invalid(form)



# Tela Exclusão Previsao Despesas
class PrevisaoDespesasDeleteViews(DeleteView):
    model = PrevisaoDespesas
    success_url = reverse_lazy("previsao_despesas_list")
   



# Tela Previsao x Realizado
class PrevisaoxRealizadoListViews(LoginRequiredMixin, ListView):
    model = PrevisaoReceitas
    template_name = 'previsao_realizado_list.html'
    context_object_name = 'previsao_realizado_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_condominio = self.request.user.n_condominio
        context['previsao_receitas'] = PrevisaoReceitas.objects.filter(n_condominio=user_condominio)
        context['previsao_despesas'] = PrevisaoDespesas.objects.filter(n_condominio=user_condominio)
        context['realizado_receitas'] = ContaReceber.objects.filter(n_condominio=user_condominio)

        # Gerar a lista de meses para o cabeçalho da tabela
        context['months'] = ['01-2024', '02-2024', '03-2024', '04-2024', '05-2024', '06-2024',
                            '07-2024', '08-2024', '09-2024', '10-2024', '11-2024', '12-2024']
        context['financeiro_estrutura'] = FinanceiroEstrutura.objects.filter(n_condominio=user_condominio)

        # Calcular Executado e percentual para cada conta
        for conta in context['financeiro_estrutura']:
            conta.executado = {}
            conta.percentual = {}
            conta.previsao = {}
            conta.realizado = {}
            for month in context['months']:
                # Convert MM-YYYY to a full date format (YYYY-MM-01)
                month_int, year_int = month.split('-')
                month_date = datetime.strptime(f"{year_int}-{month_int}-01", '%Y-%m-%d').date()

                # Obter valores de PrevisaoReceitas e Receita (se existirem)
                receita_valor = context['previsao_receitas']\
                    .filter(categoria=conta, data_orcamento_receita=month_date)\
                    .aggregate(Sum('valor_orcamento_receita'))['valor_orcamento_receita__sum']

                realizado_valor = context['realizado_receitas']\
                    .filter(categoria=conta,
                            data_recebimento__year=int(year_int),
                            data_recebimento__month=int(month_int))\
                    .aggregate(Sum('valor_recebido'))['valor_recebido__sum']

                # Se não houver valor, definir como None para o filtro funcionar corretamente
                conta.previsao[month] = receita_valor if receita_valor is not None else None
                conta.realizado[month] = realizado_valor if realizado_valor is not None else None
                conta.executado[month] = max(receita_valor - realizado_valor, 0) if receita_valor and realizado_valor else None
                conta.percentual[month] = (realizado_valor / receita_valor * 100) if receita_valor and realizado_valor else None

        return context



# Tela Execução Orçamento
class GraficosListViews(LoginRequiredMixin, ListView):
    model = PrevisaoReceitas
    template_name = 'execOrcamento.html'
    context_object_name = 'previsoes_receita'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obter o condomínio do usuário
        user_condominio = self.request.user.n_condominio

        # Verificar se o mês foi passado como parâmetro na URL
        mes = self.request.GET.get('mes')

        if mes:
            # Filtrar os valores agregados pelo mês
            total_orcamento_receita = PrevisaoReceitas.objects.filter(
                n_condominio=user_condominio,
                data_orcamento_receita__month=mes
            ).aggregate(Sum('valor_orcamento_receita'))['valor_orcamento_receita__sum'] or 0

            total_recebido_receita = ContaReceber.objects.filter(
                n_condominio=user_condominio,
                data_recebimento__month=mes
            ).aggregate(Sum('valor_recebido'))['valor_recebido__sum'] or 0

            total_orcamento_despesa = PrevisaoDespesas.objects.filter(
                n_condominio=user_condominio,
                data_orcamento_despesa__month=mes
            ).aggregate(Sum('valor_orcamento_despesa'))['valor_orcamento_despesa__sum'] or 0

            total_pago_despesa = ContaPagar.objects.filter(
                n_condominio=user_condominio,
                data_pagamento__month=mes
            ).aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0
        else:
            # Valores sem filtro de mês
            total_orcamento_receita = PrevisaoReceitas.objects.filter(n_condominio=user_condominio).aggregate(Sum('valor_orcamento_receita'))['valor_orcamento_receita__sum'] or 0
            total_recebido_receita = ContaReceber.objects.filter(n_condominio=user_condominio).aggregate(Sum('valor_recebido'))['valor_recebido__sum'] or 0
            total_orcamento_despesa = PrevisaoDespesas.objects.filter(n_condominio=user_condominio).aggregate(Sum('valor_orcamento_despesa'))['valor_orcamento_despesa__sum'] or 0
            total_pago_despesa = ContaPagar.objects.filter(n_condominio=user_condominio).aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0

        # Adicionando os valores agregados ao contexto
        context['orcamento_receita'] = total_orcamento_receita
        context['recebido_receita'] = total_recebido_receita
        context['orcamento_despesa'] = total_orcamento_despesa
        context['pago_despesa'] = total_pago_despesa

        # Retornar os dados JSON se for uma requisição AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'orcamento_receita': total_orcamento_receita,
                'recebido_receita': total_recebido_receita,
                'orcamento_despesa': total_orcamento_despesa,
                'pago_despesa': total_pago_despesa
            })

        return context







#----------------------- SUBSISTEMA PRODUTIVIDADE ....................................................................................................................


#-----------------------Views PRODUTIVIDADE.......................................................
        
# Tela Lista Produtividade 
class ProdutividadesListViews(LoginRequiredMixin, ListView):
    model = Produtividade
    context_object_name = 'produtividades_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os pets pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['produtividades_list'] = Produtividade.objects.filter(n_condominio=user_condominio)
        
        return context



# Tela Cadastra Produtividade
@method_decorator(login_required, name='dispatch')
class ProdutividadesCreateViews(CreateView):
    model = Produtividade
    fields = ["cpf_colaborador", "nome_tarefa", "local_tarefa", "tempo_execucao"]
    success_url = reverse_lazy("produtividades_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_condominio = self.request.user.n_condominio
        context['colaboradores_list'] = CustomColaborador.objects.filter(n_condominio=user_condominio)
        context['messages'] = messages.get_messages(self.request)

        return context

    def form_valid(self, form):
        # Atribui o condomínio do usuário logado ao campo n_condominio do formulário
        form.instance.n_condominio = self.request.user.n_condominio       
   
        return super().form_valid(form)

    def form_invalid(self, form):
        # Mostra uma mensagem de erro para o usuário
        messages.error(self.request, 'Erro ao inserir a atividade.')

        return self.render_to_response(self.get_context_data(form=form))



# Tela Alteração Produtividade
class ProdutividadesUpdateViews(UpdateView):
    model = Produtividade
    fields = ["nome_tarefa", "local_tarefa", "tempo_execucao"]  # Apenas o campo a ser atualizado
    context_object_name = 'produtividade'
    success_url = reverse_lazy("produtividades_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_condominio = self.request.user.n_condominio
        context['colaboradores_list'] = CustomColaborador.objects.filter(n_condominio=user_condominio)
        context['messages'] = messages.get_messages(self.request)

        return context

    def form_valid(self, form):
        # Atribui o condomínio do usuário logado ao campo n_condominio do formulário
        form.instance.n_condominio = self.request.user.n_condominio
        
        return super().form_valid(form)

    def form_invalid(self, form):
        # Mostra uma mensagem de erro para o usuário
        messages.error(self.request, 'Erro ao atualizar a atividade')
        return self.render_to_response(self.get_context_data(form=form))



# Tela Exclusão Produtividade
class ProdutividadesDeleteViews(DeleteView):
    model = Produtividade
    success_url = reverse_lazy("produtividades_list")






#----------------------- SUBSISTEMA METAS ....................................................................................................................


#-----------------------Views METAS.......................................................
        
# Tela Lista Metas 
class MetasListViews(LoginRequiredMixin, ListView):
    model = Meta
    context_object_name = 'metas_list'
    
    def get_context_data(self, **kwargs):
        # Obter o contexto base da ListView
        context = super().get_context_data(**kwargs)
        
        # Filtrar os pets pelo condomínio do usuário logado
        user_condominio = self.request.user.n_condominio
        context['metas_list'] = Meta.objects.filter(n_condominio=user_condominio, meta_executada='Não executada')

        
        return context



# Tela Cadastra Metas
@method_decorator(login_required, name='dispatch')
class MetasCreateViews(CreateView):
    model = Meta
    fields = ["cpf_colaborador", "dsc_meta", "data_termino"]
    success_url = reverse_lazy("metas_list")

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            user_condominio = self.request.user.n_condominio
            context['colaboradores_list'] = CustomColaborador.objects.filter(n_condominio=user_condominio)
            context['messages'] = messages.get_messages(self.request)

            return context

    def form_valid(self, form):
            # Atribui o condomínio do usuário logado ao campo n_condominio do formulário
            form.instance.n_condominio = self.request.user.n_condominio       
    
            return super().form_valid(form)

    def form_invalid(self, form):
            # Mostra uma mensagem de erro para o usuário
            messages.error(self.request, 'Erro ao inserir a atividade.')

            return self.render_to_response(self.get_context_data(form=form))



# Tela Alteração Metas
class MetasUpdateViews(UpdateView):
    model = Meta
    fields = ["dsc_meta", "data_termino"]  # Apenas o campo a ser atualizado
    context_object_name = 'meta'
    template_name = 'metas_update.html'
    success_url = reverse_lazy("metas_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_condominio = self.request.user.n_condominio
        context['colaboradores_list'] = CustomColaborador.objects.filter(n_condominio=user_condominio)
        context['messages'] = messages.get_messages(self.request)
        context['meta'] = self.object  # garante que 'meta' está no contexto

        return context

    def form_valid(self, form):
        # Atribui o condomínio do usuário logado ao campo n_condominio do formulário
        form.instance.n_condominio = self.request.user.n_condominio
        
        return super().form_valid(form)

    def form_invalid(self, form):
        # Mostra uma mensagem de erro para o usuário
        messages.error(self.request, 'Erro ao atualizar a meta')
        return self.render_to_response(self.get_context_data(form=form))



# Tela Exclusão Metas
class MetasDeleteViews(DeleteView):
    model = Meta
    success_url = reverse_lazy("metas_list")



# Tela Avaliação das Metas
class MetasAvaliarViews(UpdateView):
    model = Meta
    fields = ["meta_executada"]  # Apenas o campo a ser atualizado
    context_object_name = 'meta'
    template_name = 'metas_avaliar.html'
    success_url = reverse_lazy("metas_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_condominio = self.request.user.n_condominio
        context['colaboradores_list'] = CustomColaborador.objects.filter(n_condominio=user_condominio)
        context['messages'] = messages.get_messages(self.request)
        context['meta'] = self.object  # garante que 'meta' está no contexto
        context['meta_executada'] = [
            ('Executada', 'Executada'),
            ('Não executada', 'Não executada')
        ]
        return context

    def form_valid(self, form):
        # Atribui o condomínio do usuário logado ao campo n_condominio do formulário
        form.instance.n_condominio = self.request.user.n_condominio
        
        return super().form_valid(form)

    def form_invalid(self, form):
        # Mostra uma mensagem de erro para o usuário
        messages.error(self.request, 'Erro ao inserir a avaliação')
        return self.render_to_response(self.get_context_data(form=form))







#----------------------- SUBSISTEMA ENQUETE ....................................................................................................................


from django.forms import modelformset_factory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render
import json
import logging
from .models import Pergunta, PossivelResposta

logger = logging.getLogger(__name__)



@method_decorator(login_required, name='dispatch')
class EnqueteCreateView(View):
    template_name = 'enquete/enquete_create.html'
    success_url = reverse_lazy('enquete_create')

    def get(self, request, *args, **kwargs):
        user_condominio = request.user.n_condominio
        perguntas = []
        
        # Busca todas as perguntas do condomínio atual
        queryset = Pergunta.objects.filter(n_condominio=user_condominio)
        
        for pergunta in queryset:
            # Busca as respostas relacionadas a cada pergunta usando o novo nome do campo
            possiveis_respostas = pergunta.possiveis_respostas.all().values(
                'possivelResposta_id',  # Changed from resposta_id
                'texto_resposta'
            )
            
            # Monta o dicionário com os dados da pergunta
            pergunta_dict = {
                'pergunta_id': pergunta.pergunta_id,
                'texto_pergunta': pergunta.texto_pergunta,
                'status': pergunta.status,
                'multiple_responses': pergunta.multiple_responses,
                'possiveis_respostas': list(possiveis_respostas)
            }
            perguntas.append(pergunta_dict)

        context = {
            'perguntas': perguntas,
            'messages': []
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            texto_pergunta = data.get('texto_pergunta', '').strip()
            respostas = data.get('respostas', [])
            status = data.get('status', False)
            multiple_responses = data.get('multiple_responses', False)

            if not texto_pergunta:
                return JsonResponse({
                    'status': 'error',
                    'message': 'O texto da pergunta é obrigatório.'
                }, status=400)

            if not respostas:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Pelo menos uma resposta é necessária.'
                }, status=400)

            with transaction.atomic():
                # Create the poll question
                pergunta = Pergunta.objects.create(
                    texto_pergunta=texto_pergunta,
                    status=status,
                    multiple_responses=multiple_responses,
                    n_condominio=request.user.n_condominio
                )

                # Create the possible answers
                for resposta in respostas:
                    if isinstance(resposta, dict) and resposta.get('texto_resposta', '').strip():
                        PossivelResposta.objects.create(
                            pergunta=pergunta,
                            texto_resposta=resposta['texto_resposta'].strip(),
                            n_condominio=request.user.n_condominio
                        )

                return JsonResponse({
                    'status': 'success',
                    'message': 'Enquete criada com sucesso!',
                    'pergunta_id': pergunta.pergunta_id
                })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Dados inválidos enviados.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erro ao criar enquete: {str(e)}'
            }, status=500)

@method_decorator(login_required, name='dispatch')
class EnqueteDeleteView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            pergunta_id = data.get('pergunta_id')
            user_condominio = request.user.n_condominio

            if not pergunta_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'ID da enquete não fornecido.'
                }, status=400)

            with transaction.atomic():
                pergunta = Pergunta.objects.get(
                    pergunta_id=pergunta_id,
                    n_condominio=user_condominio
                )
                pergunta.delete()

            return JsonResponse({
                'status': 'success',
                'message': 'Enquete excluída com sucesso!'
            })

        except Pergunta.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Enquete não encontrada.'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

# ...existing code...

class EnqueteUpdateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            pergunta_id = data.get('pergunta_id')
            texto_pergunta = data.get('texto_pergunta', '').strip()
            respostas = data.get('respostas', [])
            status = data.get('status', False)
            multiple_responses = data.get('multiple_responses', False)

            with transaction.atomic():
                # Update the existing poll
                pergunta = Pergunta.objects.get(
                    pergunta_id=pergunta_id,
                    n_condominio=request.user.n_condominio
                )
                pergunta.texto_pergunta = texto_pergunta
                pergunta.status = status
                pergunta.multiple_responses = multiple_responses
                pergunta.save()

                # Delete existing responses
                pergunta.possiveis_respostas.all().delete()

                # Create new responses
                for resposta in respostas:
                    if isinstance(resposta, dict) and resposta.get('texto_resposta', '').strip():
                        PossivelResposta.objects.create(
                            pergunta=pergunta,
                            texto_resposta=resposta['texto_resposta'].strip(),
                            n_condominio=request.user.n_condominio
                        )

                return JsonResponse({
                    'status': 'success',
                    'message': 'Enquete atualizada com sucesso!'
                })

        except Pergunta.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Enquete não encontrada.'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erro ao atualizar enquete: {str(e)}'
            }, status=500)

# ...existing code...

class VotacaoView(LoginRequiredMixin, View):
    template_name = 'enquete/Votacao.html'

    def get(self, request):
        user_condominio = request.user.n_condominio
        perguntas = []
        already_voted_perguntas = set()
        
        try:
            # Get condomino instance
            condomino = CustomCondomino.objects.get(
                cpf_condomino=request.user.cpf_usuario,
                n_condominio=user_condominio
            )
            
            # Get all questions this user has already voted on
            voted_perguntas = Resposta.objects.filter(
                cpf_condomino=condomino,
                n_condominio=user_condominio
            ).values_list('pergunta_id', flat=True)
            
            already_voted_perguntas = set(voted_perguntas)
        except CustomCondomino.DoesNotExist:
            messages.error(request, 'Condômino não encontrado')
            return redirect('home')
        
        # Busca todas as perguntas ativas do condomínio atual
        queryset = Pergunta.objects.filter(
            n_condominio=user_condominio,
            status=True
        ).prefetch_related('possiveis_respostas')
        
        for pergunta in queryset:
            # Busca as respostas possíveis para cada pergunta
            possiveis_respostas = list(pergunta.possiveis_respostas.filter(
                n_condominio=user_condominio
            ).values('possivelResposta_id', 'texto_resposta'))
            
            # Check if user has already voted on this question
            already_voted = pergunta.pergunta_id in already_voted_perguntas
            
            # Monta o dicionário com os dados da pergunta
            pergunta_dict = {
                'pergunta_id': pergunta.pergunta_id,
                'texto_pergunta': pergunta.texto_pergunta,
                'multiple_responses': pergunta.multiple_responses,
                'possiveis_respostas': possiveis_respostas,
                'already_voted': already_voted
            }
            perguntas.append(pergunta_dict)

        context = {
            'perguntas': perguntas,
            'messages': messages.get_messages(request)
        }
        
        return render(request, self.template_name, context)

class VotacaoSubmitView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            respostas_data = data.get('respostas', [])
            
            if not respostas_data:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Nenhuma resposta fornecida.'
                }, status=400)

            user_condominio = request.user.n_condominio
            
            try:
                condomino = CustomCondomino.objects.get(
                    cpf_condomino=request.user.cpf_usuario,
                    n_condominio=user_condominio
                )
            except CustomCondomino.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Condômino não encontrado.'
                }, status=400)
            
            with transaction.atomic():
                for resposta_item in respostas_data:
                    pergunta_id = resposta_item.get('pergunta_id')
                    respostas_selecionadas = resposta_item.get('respostas', [])
                    
                    # Skip if already voted
                    if Resposta.objects.filter(
                        pergunta_id=pergunta_id,
                        cpf_condomino=condomino,
                        n_condominio=user_condominio
                    ).exists():
                        continue
                    
                    try:
                        pergunta = Pergunta.objects.get(
                            pergunta_id=pergunta_id,
                            n_condominio=user_condominio,
                            status=True
                        )
                    except Pergunta.DoesNotExist:
                        continue
                    
                    for resposta_id in respostas_selecionadas:
                        try:
                            possivel_resposta = PossivelResposta.objects.get(
                                possivelResposta_id=resposta_id,
                                pergunta=pergunta,
                                n_condominio=user_condominio
                            )
                            
                            Resposta.objects.create(
                                pergunta=pergunta,
                                possivel_resposta=possivel_resposta,
                                cpf_condomino=condomino,
                                n_condominio=user_condominio
                            )
                        except PossivelResposta.DoesNotExist:
                            continue
            
            return JsonResponse({
                'status': 'success',
                'message': 'Voto registrado com sucesso!'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Dados inválidos enviados.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erro ao registrar voto: {str(e)}'
            }, status=500)

# ...existing code...

class VotacaoRespostasView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            user_condominio = request.user.n_condominio
            
            # Get condomino instance using cpf_usuario instead of cpf_condominio
            condomino = CustomCondomino.objects.get(
                cpf_condomino=request.user.cpf_usuario,
                n_condominio=user_condominio
            )
            
            # Get all responses for this condomino
            respostas = Resposta.objects.filter(
                cpf_condomino=condomino,
                n_condominio=user_condominio
            ).values('pergunta_id', 'possivel_resposta_id')
            
            return JsonResponse({
                'status': 'success',
                'respostas': list(respostas)
            })
            
        except CustomCondomino.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Condômino não encontrado'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

# ...existing code...


