from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import CustomUser, CustomCondominio, CustomCondomino, CustomMorador, CustomBloco, CustomUnidade    
from .models import CustomVeiculo, CustomColaborador, CustomGaragem, CustomMudanca, CustomOcorrencia, CustomBeneficio
from .models import CustomBeneficioRecebido, CustomCorrespondencia, CustomEspacoAdm, CustomTipoPatrimonio
from .models import CustomPatrimonio
from .models import FinanceiroEstrutura, Receita, Despesas
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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
                # messages.info(request, f"{usuario}")
                return redirect('exibirHome')  # Redirect to the home page after successful login
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Por favor, forneça usuário e senha válidos.')

    # If not a POST request or authentication fails, render the login page again
    return render(request, 'login/login.html')            

# Exibe Home
def exibirHome(request):
    
    return render(request,'login/home.html')


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
            form.errors['username'] = ['Nome de usuário já existe. Escolha outro nome.']
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
class CondominosListViews(ListView):
    model = CustomCondomino
    context_object_name = 'condominos_list'


# Tela Cadastro de Condôminos
class CondominosCreateViews(CreateView):
    model = CustomCondomino
    fields = ["cpf_condomino", "nome_condomino", "telefone_condomino", "celular_condomino", "email_condomino", "data_aquisicao_imovel", "data_nascimento_condomino", "n_condominio"]
    success_url = reverse_lazy("condominos_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def form_valid(self, form):
        # Strip mask from CPF
        cpf_condomino = str(form.cleaned_data['cpf_condomino']).replace(".", "").replace("-", "")
        form.instance.cpf_condomino = cpf_condomino

        # Get the selected condominio instance
        condominio_instance = form.cleaned_data['n_condominio']

        # Assign the primary key of the selected condominium to the field
        form.instance.n_condominio_id = condominio_instance.n_condominio

        # Check if the selected condominium number exists
        if not CustomCondominio.objects.filter(n_condominio=form.instance.n_condominio_id).exists():
            messages.error(self.request, 'Número de condomínio inválido.')
            return self.form_invalid(form)
       
        # Verifica se o condômino já está cadastrado
        if CustomCondomino.objects.filter(cpf_condomino=cpf_condomino).exists():
            messages.error(self.request, 'Condômino já cadastrado')
            return self.form_invalid(form)

        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Customize error message for existing username
        if 'cpf_condomino' in form.errors:
            form.errors['cpf_condomino'] = ['Condômino já cadastrado']
        return super().form_invalid(form)
    

# Tela Alteração De Condôminos
class CondominosUpdateViews(UpdateView):
    model = CustomCondomino
    context_object_name = 'condominos_list'    
    fields = ["cpf_condomino", "nome_condomino", "data_nascimento_condomino", "telefone_condomino", "celular_condomino", "email_condomino", "data_aquisicao_imovel", "n_condominio"]
    success_url = reverse_lazy("condominos_list")
    widgets = {
        'n_condominio': forms.Select(attrs={'class': 'form-control'}),
    }
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()        
        return context
    
    def form_valid(self, form):
        # Strip mask from CPF
        cpf_condomino = str(form.cleaned_data['cpf_condomino']).replace(".", "").replace("-", "")
        form.instance.cpf_condomino = cpf_condomino
        
        # Get the selected condominium instance
        condominio_instance = form.cleaned_data['n_condominio']

        # Assign the primary key of the selected condominium to the field
        form.instance.n_condominio_id = condominio_instance.n_condominio

        # Check if the selected condominium number exists
        if not CustomCondominio.objects.filter(n_condominio=form.instance.n_condominio_id).exists():
            messages.error(self.request, 'Número de condomínio inválido.')
            return self.form_invalid(form)
        
        return super().form_valid(form)         
    
# Tela Exclusão De Condôminos
class CondominosDeleteViews(DeleteView):
    model = CustomCondomino
    success_url = reverse_lazy("condominos_list")


#-----------------------Views Condomínios.................................................................

# Tela Lista Condomínios
class CondominiosListViews(ListView):
    model = CustomCondominio
    context_object_name = 'condominios_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context


# Tela Cadastro De Condomínios
class CondominiosCreateViews(CreateView):
    model = CustomCondominio
    template_name = 'condominios_create.html'
    fields = ["n_condominio", "nome_condominio"]
    success_url = reverse_lazy("condominios_list")
    # widgets = {
    #     'n_condominio': forms.Select(attrs={'class': 'form-control'}),
    # }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context    
    
    def form_invalid(self, form):
        # Customize error message for existing username
        if 'username' in form.errors:
            form.errors['username'] = ['Número do Condomínio já existe. Defina outro número.']
        return super().form_invalid(form)
    

# Tela Alteração De Condomínios
class CondominiosUpdateViews(UpdateView):
    model = CustomCondominio
    context_object_name = 'condominios_list'
    fields = ["n_condominio", "nome_condominio"]
    success_url = reverse_lazy("condominios_list") 
    # widgets = {
    #     'n_condominio': forms.Select(attrs={'class': 'form-control'}),
    # }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context      

# Tela Exclusão De Condomínios
class CondominiosDeleteViews(DeleteView):
    model = CustomCondominio
    success_url = reverse_lazy("condominios_list")
    

#-----------------------Views Moradores.................................................................

# Tela Lista Moradores
class MoradoresListViews(ListView):
    model = CustomMorador
    context_object_name = 'moradores_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['moradores'] = CustomMorador.objects.all()
        return context

# Tela Verifica Moradores
def verificar_cpf_condomino(request):
    if request.method == 'POST':
        cpf_condomino = request.POST.get('cpf_condomino')
        cpf_condomino = cpf_condomino.replace(".", "").replace("-", "")  # Remove mask

        if CustomCondomino.objects.filter(cpf_condomino=cpf_condomino).exists():
            # CPF do condômino existe, redirecionar para moradores_create.html
            return redirect(reverse('moradores_create') + f'?cpf_condomino={cpf_condomino}')
            # return render(request, 'moradores/moradores_create.html', {'cpf_condomino': cpf_condomino})
        else:
            # CPF do condômino não encontrado, retornar para moradores_verify.html
            message = "Condômino não encontrado"
            return render(request, 'moradores/moradores_verify.html', {'message': message})
    
    # Se não for POST, retornar para moradores_verify.html
    return render(request, 'moradores/moradores_verify.html')


# Tela Cadastro De Moradores
class MoradoresCreateViews(CreateView):
    model = CustomMorador
    template_name = 'moradores_create.html'
    fields = ["cpf_condomino", "cpf_morador", "nome_morador", "data_nascimento_morador", "celular_morador", "email_morador", "parentesco_condomino"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominos'] = CustomCondomino.objects.all()
        return context

    def form_valid(self, form):
        # Extract the cpf_condomino value from the form
        cpf_condomino_obj = form.cleaned_data['cpf_condomino']
        cpf_condomino_str = str(cpf_condomino_obj.cpf_condomino).replace(".", "").replace("-", "")
        print("CPF Condômino:", cpf_condomino_str)

        # Remove máscara do CPF do morador
        cpf_morador = form.cleaned_data['cpf_morador'].replace(".", "").replace("-", "")
        print("CPF Morador:", cpf_morador)
        form.instance.cpf_morador = cpf_morador
        
        # Verifica se o CPF do morador já está cadastrado
        if CustomMorador.objects.filter(cpf_morador=cpf_morador).exists():
            messages.error(self.request, 'Morador já cadastrado')
            return self.form_invalid(form)
        
        # Verifica se o CPF do condômino já está cadastrado
        condomino = CustomCondomino.objects.filter(cpf_condomino=cpf_condomino_str).first()
        print("Queryset result:", condomino)
        if not condomino:
            messages.error(self.request, 'CPF de condômino não encontrado.')
            return self.form_invalid(form)
            
        # Assign the condomínio to the morador
        form.instance.cpf_condomino = condomino
        form.instance.n_condominio = condomino.n_condominio

        self.object = form.save()
        
        # Recarrega página com o mesmo cpf
        return redirect(reverse('moradores_create') + f'?cpf_condomino={cpf_condomino_str}')    

    def form_invalid(self, form):
        return super().form_invalid(form)
        

# Tela Alteração De Moradores
class MoradoresUpdateViews(UpdateView):
    model = CustomMorador
    template_name = 'moradores/moradores_update.html'
    context_object_name = 'morador'
    fields = ["cpf_condomino", "cpf_morador", "nome_morador", "data_nascimento_morador", "celular_morador", "email_morador", "parentesco_condomino", "n_condominio"]
    success_url = reverse_lazy("moradores_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['condominos'] = CustomCondomino.objects.all()
        return context

    def form_valid(self, form):
        # Get the selected condominium instance
        condominio_instance = form.cleaned_data['n_condominio']
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


# Tela Exclusão De Moradores

class MoradoresDeleteViews(DeleteView):
    model = CustomMorador
    template_name = 'moradores/moradores_confirm_delete.html'
    success_url = reverse_lazy('moradores_list')


    #-----------------------Views Blocos.................................................................

# Tela Lista os Blocos
class BlocosListViews(ListView):
    model = CustomBloco
    context_object_name = 'blocos_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blocos'] = CustomBloco.objects.all()
        return context


# Tela Cadastro de Blocos 
class BlocosCreateViews(CreateView):
    model = CustomBloco
    template_name = 'blocos_create.html'
    fields = ["bloco", "n_condominio"]
    success_url = reverse_lazy("blocos_list")

    # rotinas para gerar as informações na div do select no html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def form_valid(self, form):
        condominio_instance = form.cleaned_data['n_condominio']
        form.instance.n_condominio_id = condominio_instance.n_condominio

        if not CustomCondominio.objects.filter(n_condominio=form.instance.n_condominio_id).exists():
            form.add_error('n_condominio', 'Número de condomínio inválido.')
            return self.form_invalid(form)

        bloco_instance = form.cleaned_data['bloco']
        form.instance.bloco = bloco_instance

        # Verificar se a combinação bloco-condomínio já existe
        if CustomBloco.objects.filter(bloco=form.instance.bloco, n_condominio=form.instance.n_condominio_id).exists():
            form.add_error('bloco', 'Bloco já cadastrado para este condomínio.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


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
        return super().form_invalid(form)
    
       
# Tela Exclusão de Blocos
class BlocosDeleteViews(DeleteView):
    model = CustomBloco
    success_url = reverse_lazy("blocos_list")
    # template_name = 'App_SGC\templates\Blocos\blocos_confirm_delete.html'  
   


  #-----------------------Views Unidades.................................................................

# Tela Lista as Unidades 
class UnidadesListViews(ListView):
    model = CustomUnidade
    context_object_name = 'unidades_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unidades'] = CustomUnidade.objects.all()
        return context    


# Tela Cadastro de Unidades
class UnidadesCreateViews(View):
    template_name = 'unidades/unidades_create.html'
    success_url = reverse_lazy("unidades_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['blocos'] = CustomBloco.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        cpf_condomino = request.POST.get('cpf_condomino')
        bloco_id = request.POST.get('bloco_id')
        unidade = request.POST.get('unidade')

        context = self.get_context_data()

        # Validar CPF do condômino
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino)
        except CustomCondomino.DoesNotExist:
            context['form_errors'] = {'cpf_condomino': ' - CPF não cadastrado'}
            return render(request, self.template_name, context)
        
        # Obter a instância do condomínio associada ao condômino
        condominio_instance = condomino_instance.n_condominio
        
        # Validar se a unidade já existe para o bloco
        if CustomUnidade.objects.filter(bloco_id=bloco_id, unidade=unidade).exists():
            context['form_errors'] = {'unidade': ' - Unidade já cadastrada para este bloco'}
            return render(request, self.template_name, context)

        # Criar a nova unidade
        CustomUnidade.objects.create(
            cpf_condomino=condomino_instance,
            bloco_id=CustomBloco.objects.get(bloco_id=bloco_id),
            n_condominio=condominio_instance,
            unidade=unidade
        )        
        return HttpResponseRedirect(self.success_url)


# Tela Alteração das Unidades
class UnidadesUpdateViews(View):
    template_name = 'unidades/unidades_update.html'
    success_url = reverse_lazy("unidades_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['blocos'] = CustomBloco.objects.all()
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
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=unidade.cpf_condomino.cpf_condomino)
        except CustomCondomino.DoesNotExist:
            context['form_errors'] = {'CPF do condômino não cadastrado'}
            return render(request, self.template_name, context)
        
        # Obter a instância do condomínio associada ao condômino
        condominio_instance = condomino_instance.n_condominio
        
        # Validar se a unidade já existe para o bloco
        if CustomUnidade.objects.filter(bloco_id=bloco_id, unidade=unidade_str).exists():
            context['form_errors'] = {'unidade': ' - Unidade já cadastrada para este bloco'}
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
class VeiculosListViews(ListView):
    model = CustomVeiculo
    template_name = 'veiculos/veiculos_list.html'
    context_object_name = 'veiculo_list'

    
# Tela Cadastro de Veículos
class VeiculosCreateViews(View):
    template_name = 'veiculos/veiculos_create.html'
    success_url = reverse_lazy("veiculos_list")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        context = {}
        form_errors = {}

        cpf_condomino = request.POST.get('cpf_condomino')
        placa_veiculo = request.POST.get('placa_veiculo')
        marca_veiculo = request.POST.get('marca_veiculo')
        modelo_veiculo = request.POST.get('modelo_veiculo')
        cor_veiculo = request.POST.get('cor_veiculo')

        # Validar CPF do condômino
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino)
        except CustomCondomino.DoesNotExist:
            form_errors['cpf_condomino'] = 'Condômino não cadastrado'

        # Verificar se a placa do veículo foi digitada
        if not placa_veiculo:
            form_errors['placa_veiculo'] = 'Digite a placa do veículo'
        
        # Verificar se a marca do veículo foi digitada
        if not marca_veiculo:
            form_errors['marca_veiculo'] = 'Digite a marca do veículo'
        
        # Verificar se o modelo do veículo foi digitado
        if not modelo_veiculo:
            form_errors['modelo_veiculo'] = 'Digite o modelo do veículo'
        
        # Verificar se a cor do veículo foi digitada
        if not cor_veiculo:
            form_errors['cor_veiculo'] = 'Digite a cor do veículo'

        # Verificar se há erros de formulário
        if form_errors:
            context['form_errors'] = form_errors
            return render(request, self.template_name, context)

        # Validar se o veículo já está cadastrado
        if CustomVeiculo.objects.filter(placa_veiculo=placa_veiculo).exists():
            form_errors['placa_veiculo'] = 'Veículo já cadastrado'
            context['form_errors'] = form_errors
            return render(request, self.template_name, context)

        # Inserir os dados na tabela CustomVeiculo
        try:
            veiculo = CustomVeiculo(
                placa_veiculo=placa_veiculo,
                marca_veiculo=marca_veiculo,
                modelo_veiculo=modelo_veiculo,
                cor_veiculo=cor_veiculo,
                cpf_condomino=condomino_instance
            )
            veiculo.save()
        except Exception as e:
            form_errors['general'] = 'Erro ao inserir o veículo'
            context['form_errors'] = form_errors
            return render(request, self.template_name, context)

        return redirect(self.success_url)


# Tela Alteração de Veículos
class VeiculosUpdateViews(View):
    template_name = 'veiculos/veiculos_update.html'
    success_url = reverse_lazy("veiculos_list")

    def get(self, request, *args, **kwargs):
        veiculo = get_object_or_404(CustomVeiculo, pk=kwargs['pk'])
        context = {
            'veiculo': veiculo
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form_errors = {}
        veiculo = get_object_or_404(CustomVeiculo, pk=kwargs['pk'])

        cpf_condomino = request.POST.get('cpf_condomino')
        placa_veiculo = request.POST.get('placa_veiculo')
        marca_veiculo = request.POST.get('marca_veiculo')
        modelo_veiculo = request.POST.get('modelo_veiculo')
        cor_veiculo = request.POST.get('cor_veiculo')

        # Validar CPF do condômino
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino)
        except CustomCondomino.DoesNotExist:
            form_errors['cpf_condomino'] = 'Condômino não cadastrado'

        # Verificar se a placa do veículo foi digitada
        if not placa_veiculo:
            form_errors['placa_veiculo'] = 'Digite a placa do veículo'
        
        # Verificar se a marca do veículo foi digitada
        if not marca_veiculo:
            form_errors['marca_veiculo'] = 'Digite a marca do veículo'
        
        # Verificar se o modelo do veículo foi digitado
        if not modelo_veiculo:
            form_errors['modelo_veiculo'] = 'Digite o modelo do veículo'
        
        # Verificar se a cor do veículo foi digitada
        if not cor_veiculo:
            form_errors['cor_veiculo'] = 'Digite a cor do veículo'

        # Verificar se há erros de formulário
        if form_errors:
            context['form_errors'] = form_errors
            context['veiculo'] = veiculo
            return render(request, self.template_name, context)

        # Atualiza os dados do veículo
        veiculo.marca_veiculo = marca_veiculo
        veiculo.modelo_veiculo = modelo_veiculo
        veiculo.cor_veiculo = cor_veiculo
        veiculo.cpf_condomino = condomino_instance

        try:
            veiculo.save()
        except Exception as e:
            form_errors['general'] = 'Erro ao atualizar o veículo'
            context['form_errors'] = form_errors
            context['veiculo'] = veiculo
            return render(request, self.template_name, context)

        return redirect(self.success_url)
    

# Tela Exclusão de Veículo
class VeiculosDeleteViews(DeleteView):
    model = CustomVeiculo
    success_url = reverse_lazy("veiculos_list")


#-----------------------Views Colaborador.................................................................

# Tela Lista Colaborador
class ColaboradoresListViews(ListView):
    model = CustomColaborador
    context_object_name = 'colaboradores_list'


# Tela Cadastro de Colaborador
class ColaboradoresCreateViews(CreateView):
    model = CustomColaborador
    fields = ["cpf_colaborador", "nome_colaborador", "data_nascimento_colaborador", "endereco_colaborador", "telefone_colaborador", "celular_colaborador", "email_colaborador", "nome_contato_colaborador", "celular_contato_colaborador", "n_condominio"]
    success_url = reverse_lazy("colaboradores_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def form_valid(self, form):
        # Strip mask from CPF
        cpf_colaborador = str(form.cleaned_data['cpf_colaborador']).replace(".", "").replace("-", "")
        form.instance.cpf_colaborador = cpf_colaborador

        # Get the selected condominio instance
        colaborador_instance = form.cleaned_data['n_condominio']

        # Assign the primary key of the selected condominium to the field
        form.instance.n_condominio_id = colaborador_instance.n_condominio

        # Check if the selected condominium number exists
        if not CustomCondominio.objects.filter(n_condominio=form.instance.n_condominio_id).exists():
            messages.error(self.request, 'Número de condomínio inválido.')
            return self.form_invalid(form)
       
        # Verifica se o condômino já está cadastrado
        if CustomColaborador.objects.filter(cpf_colaborador=cpf_colaborador).exists():
            messages.error(self.request, 'Colaborador já cadastrado')
            return self.form_invalid(form)

        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Customize error message for existing username
        if 'cpf_colaborador' in form.errors:
            form.errors['cpf_colaborador'] = ['Colaborador já cadastrado']
        return super().form_invalid(form)
    

# Tela Alteração De Colaborador
class ColaboradoresUpdateViews(UpdateView):
    model = CustomColaborador
    template_name = 'colaboradores/colaboradores_update.html'
    context_object_name = 'colaborador'
    fields = ["cpf_colaborador", "nome_colaborador", "data_nascimento_colaborador", "endereco_colaborador", "telefone_colaborador", "celular_colaborador", "email_colaborador", "nome_contato_colaborador", "celular_contato_colaborador", "n_condominio"]
    success_url = reverse_lazy("colaboradores_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context
    
    def form_valid(self, form):
        # Strip mask from CPF
        cpf_colaborador = str(form.cleaned_data['cpf_colaborador']).replace(".", "").replace("-", "")
        form.instance.cpf_colaborador = cpf_colaborador
        
        # Get the selected condominium instance
        condominio_instance = form.cleaned_data['n_condominio']

        # Assign the primary key of the selected condominium to the field
        form.instance.n_condominio_id = condominio_instance.n_condominio

        # Check if the selected condominium number exists
        if not CustomCondominio.objects.filter(n_condominio=form.instance.n_condominio_id).exists():
            messages.error(self.request, 'Número de condomínio inválido.')
            return self.form_invalid(form)
        
        return super().form_valid(form)
        
    
# Tela Exclusão De Colaborador
class ColaboradoresDeleteViews(DeleteView):
    model = CustomColaborador
    success_url = reverse_lazy("colaboradores_list")


#-----------------------Views Garagens.................................................................

# Tela Lista Garagem
class GaragensListViews(ListView):
    model = CustomGaragem
    context_object_name = 'garagens_list'


# Tela Cadastro Garagem
class GaragensCreateViews(View):
    template_name = 'garagens/garagens_create.html'
    success_url = reverse_lazy("garagens_list")

    # Busca informações dos Blocos para o Select
    def get_context_data(self, **kwargs):
        context = {}
        context['blocos'] = CustomBloco.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        cpf_condomino = request.POST.get('cpf_condomino')
        bloco_id = request.POST.get('bloco_id')
        n_garagem = request.POST.get('n_garagem')

        context = self.get_context_data()

        # Validar CPF do condômino
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino)
        except CustomCondomino.DoesNotExist:
            context['form_errors'] = {'CPF não cadastrado'}
            return render(request, self.template_name, context)
        
        # Obter a instância do condomínio associada ao condômino
        condominio_instance = condomino_instance.n_condominio
        
        # Validar se a garagem já existe para o bloco
        if CustomGaragem.objects.filter(bloco_id=bloco_id, n_garagem=n_garagem).exists():
            context['form_errors'] = {'Garagem já cadastrada para este bloco'}
            return render(request, self.template_name, context)

        # Criar a nova unidade
        CustomGaragem.objects.create(
            cpf_condomino=condomino_instance,
            bloco_id=CustomBloco.objects.get(bloco_id=bloco_id),
            n_condominio=condominio_instance,
            n_garagem=n_garagem
        )        
        return HttpResponseRedirect(self.success_url)

    
# Tela Alteração Garagem
class GaragensUpdateViews(View):
    template_name = 'garagens/garagens_update.html'
    success_url = reverse_lazy("garagens_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['blocos'] = CustomBloco.objects.all()
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

        # Validar CPF do condômino
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino)
        except CustomCondomino.DoesNotExist:
            context['form_errors'] = {'CPF não cadastrado'}
            return render(request, self.template_name, context)

        # Obter a instância do condomínio associada ao condômino
        condominio_instance = condomino_instance.n_condominio

        # Validar se a garagem já existe para o bloco
        if CustomGaragem.objects.filter(bloco_id=bloco_id, n_garagem=n_garagem).exists():
            context['form_errors'] = {'Garagem já cadastrada para este bloco'}
            return render(request, self.template_name, context)

        # Atualizar a unidade existente
        garagem = CustomGaragem.objects.get(pk=self.kwargs['pk'])
        garagem.cpf_condomino = condomino_instance
        garagem.bloco_id = CustomBloco.objects.get(bloco_id=bloco_id)
        garagem.n_condominio = condominio_instance
        garagem.n_garagem = n_garagem
        garagem.save()

        return redirect(self.success_url)

# Tela Exclusão de Garagem
class GaragensDeleteViews(DeleteView):
    model = CustomGaragem
    success_url = reverse_lazy("garagens_list")


#-----------------------Views Mudanças.................................................................

# Tela Lista as Mudanças 
class MudancasListViews(ListView):
    model = CustomMudanca
    context_object_name = 'mudancas_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mudancas'] = CustomMudanca.objects.all()
        return context    
 

# Tela Cadastro de Mudanças
class MudancasCreateViews(View):
    template_name = 'mudancas/mudancas_create.html'
    success_url = reverse_lazy("mudancas_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['blocos'] = CustomBloco.objects.all()
        context['unidades'] = CustomUnidade.objects.all()  # Adiciona as unidades ao contexto
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        cpf_condomino = request.POST.get('cpf_condomino')
        bloco_id = request.POST.get('bloco_id')
        unidade_id = request.POST.get('unidade_id')
        data_mudanca = request.POST.get('data_mudanca')
        hora_mudanca = request.POST.get('hora_mudanca')
        transportadora = request.POST.get('transportadora')

        context = self.get_context_data()

        # Validar CPF do condômino
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino)
        except CustomCondomino.DoesNotExist:
            context['form_errors'] = {'CPF não cadastrado'}
            return render(request, self.template_name, context)

        # Obter a instância do condomínio associada ao condômino
        condominio_instance = condomino_instance.n_condominio

        # Insere na tabela mudança nova linha
        CustomMudanca.objects.create(
            cpf_condomino=condomino_instance,
            bloco_id=CustomBloco.objects.get(bloco_id=bloco_id),
            unidade_id=CustomUnidade.objects.get(unidade_id=unidade_id),
            data_mudanca=data_mudanca,
            hora_mudanca=hora_mudanca,
            transportadora=transportadora,
            placa_veiculo_transportadora=request.POST.get('placa_veiculo_transportadora'),
            n_condominio=condominio_instance,
        )
        return HttpResponseRedirect(self.success_url)


# Tela Alteração das Mudanças
class MudancasUpdateViews(UpdateView):
    model = CustomMudanca
    template_name = 'mudancas/mudancas_update.html'
    context_object_name = 'mudanca'
    fields = [
        "mudanca_id", "data_mudanca", "hora_mudanca", "transportadora", 
        "placa_veiculo_transportadora", "bloco_id", 
        "unidade_id", "n_condominio"
    ]
    success_url = reverse_lazy("mudancas_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['blocos'] = CustomBloco.objects.all()
        context['unidades'] = CustomUnidade.objects.all()

        mudanca = self.get_object()
        try:
            unidade = CustomUnidade.objects.get(pk=mudanca.unidade_id.pk)
            condomino = unidade.cpf_condomino
            context['cpf_usuario'] = condomino.cpf_condomino
        except CustomUnidade.DoesNotExist:
            context['cpf_usuario'] = ''

        return context

    def form_valid(self, form):
        condominio_instance = form.cleaned_data.get('n_condominio')

        form.instance.n_condominio_id = condominio_instance.n_condominio if condominio_instance else None

        if not CustomCondominio.objects.filter(n_condominio=form.instance.n_condominio_id).exists():
            messages.error(self.request, 'Número de condomínio inválido.')
            return self.form_invalid(form)

        return super().form_valid(form)
    

# Tela Exclusão das Mudanças
class MudancasDeleteViews(DeleteView):
    model = CustomMudanca
    success_url = reverse_lazy("mudancas_list")


#-----------------------Views Ocorrências.................................................................

# Tela Lista as Ocorrências 
class OcorrenciasListViews(ListView):
    model = CustomOcorrencia
    context_object_name = 'ocorrencias_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ocorrencias'] = CustomOcorrencia.objects.all()
        return context    
 

# Tela Cadastro de Ocorrências
class OcorrenciasCreateViews(View):
    template_name = 'ocorrencias/ocorrencias_create.html'
    success_url = reverse_lazy("ocorrencias_list")
    
    def get_context_data(self, **kwargs):
        context = {}   
        context['condominios'] = CustomCondominio.objects.all()
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
        n_condominio_id = request.POST.get('n_condominio')

        context = self.get_context_data()
        
        
        # Obter a instância do condômino associada ao ID do condômino
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino)
            
        except CustomCondomino.DoesNotExist:
            context['form_errors'] = {'cpf_condomino': 'test não cadastrado'}
            return render(request, self.template_name, context)

        # Obter a instância do condomínio associada ao ID do condomínio
        try:
            condominio_instance = CustomCondominio.objects.get(n_condominio=n_condominio_id)
        except CustomCondominio.DoesNotExist:
            context['form_errors'] = {'n_condominio': 'Condomínio não cadastrado'}
            return render(request, self.template_name, context)

        # Insere na tabela ocorrência nova linha
        CustomOcorrencia.objects.create(
            cpf_condomino=condomino_instance,
            data_ocorrencia=data_ocorrencia,
            hora_ocorrencia=hora_ocorrencia,
            dsc_ocorrencia=dsc_ocorrencia,
            documento_ocorrencia=documento_ocorrencia,
            n_condominio=condominio_instance
        )
        return HttpResponseRedirect(self.success_url)


# Tela Alteração das Ocorrências
class OcorrenciasUpdateViews(UpdateView):
    model = CustomOcorrencia
    template_name = 'ocorrencias/ocorrencias_update.html'
    context_object_name = 'ocorrencia'
    fields = [
        "data_ocorrencia", "hora_ocorrencia", "dsc_ocorrencia", "documento_ocorrencia", 
        "cpf_condomino", "n_condominio"
    ]
    success_url = reverse_lazy("ocorrencias_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        cpf_condomino = form.cleaned_data['cpf_condomino']
        n_condominio_id = form.cleaned_data['n_condominio']

        # Obter a instância do condômino associada ao CPF do condômino
        try:
            condomino_instance = CustomCondomino.objects.get(cpf_condomino=cpf_condomino)
        except CustomCondomino.DoesNotExist:
            form.add_error('cpf_condomino', 'CPF não cadastrado')
            return self.form_invalid(form)

        # Obter a instância do condomínio associada ao ID do condomínio
        try:
            condominio_instance = CustomCondominio.objects.get(n_condominio=n_condominio_id)
        except CustomCondominio.DoesNotExist:
            form.add_error('n_condominio', 'Condomínio não cadastrado')
            return self.form_invalid(form)

        self.object.cpf_condomino = condomino_instance
        self.object.n_condominio = condominio_instance
        self.object.save()
        return super().form_valid(form)



# Tela Exclusão das Ocorrências
class OcorrenciasDeleteViews(DeleteView):
    model = CustomOcorrencia
    success_url = reverse_lazy("mudancas_list")


#-----------------------Views Benefícios.................................................................

# Tela Lista os Benefícios 
class BeneficiosListViews(ListView):
    model = CustomBeneficio
    context_object_name = 'beneficios_list'
    template_name = 'beneficios/beneficios_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficios'] = CustomBeneficio.objects.all()
        return context   
 

# Tela Cadastro de Benefícios
class BeneficiosCreateViews(View):
    template_name = 'beneficios/beneficios_create.html'
    success_url = reverse_lazy("beneficios_list")

    # Obtém dados do condomínio p a caixa select
    def get_context_data(self, **kwargs):
        context = {}   
        context['condominios'] = CustomCondominio.objects.all()
        return context

    # Obtém dados de contexto e renderiza um template HTML com esses dados
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    # Estrutura as informações para inserir na tabela nova linha
    def post(self, request, *args, **kwargs):
        nome_beneficio = request.POST.get('nome_beneficio')
        n_condominio_id = request.POST.get('n_condominio')  # Obtém o valor do ID do condomínio a partir do formulário
        context = self.get_context_data()

        # Obter a instância do condomínio associada ao ID do condomínio
        try:
            condominio_instance = CustomCondominio.objects.get(pk=n_condominio_id)
        except CustomCondominio.DoesNotExist:
            context['form_errors'] = {'n_condominio': 'Condomínio não cadastrado'}
            return render(request, self.template_name, context)        
        
        # Insere na tabela ocorrência nova linha
        CustomBeneficio.objects.create(
            nome_beneficio=nome_beneficio,       
            n_condominio=condominio_instance
        )
        return HttpResponseRedirect(self.success_url)


# Tela Alteração dos Benefícios
class BeneficiosUpdateViews(UpdateView):
    model = CustomBeneficio
    template_name = 'beneficios/beneficios_update.html'
    context_object_name = 'beneficio'
    fields = ["nome_beneficio", "n_condominio"]
    success_url = reverse_lazy("beneficios_list")

    
# Tela Exclusão de Benefícios
class BeneficiosDeleteViews(DeleteView):
    model = CustomBeneficio
    success_url = reverse_lazy("beneficios_list")    
    


#-----------------------Views Benefícios recebidos pelos colaboradores....................................

# Tela Lista os Benefícios recebidos
class BeneficiosRecebidosListViews(ListView):
    model = CustomBeneficioRecebido
    context_object_name = 'beneficios_recebidos_list'
    template_name = 'beneficios_recebidos/beneficios_recebidos_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beneficios_recebidos'] = CustomBeneficioRecebido.objects.all()
        return context   


# Tela Cadastro de Benefícios recebidos
class BeneficiosRecebidosCreateViews(View):
    template_name = 'beneficios_recebidos/beneficios_recebidos_create.html'
    success_url = reverse_lazy("beneficios_recebidos_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['condominios'] = CustomCondominio.objects.all()
        context['beneficios'] = CustomBeneficio.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        cpf_colaborador_id = request.POST.get('cpf_colaborador')
        beneficio_id = request.POST.get('beneficio_id')
        n_condominio_id = request.POST.get('n_condominio')
        context = self.get_context_data()

        # try:
        colaborador_instance = CustomColaborador.objects.get(pk=cpf_colaborador_id)
        condominio_instance = CustomCondominio.objects.get(pk=n_condominio_id)
        beneficio_instance = CustomBeneficio.objects.get(pk=beneficio_id)

        CustomBeneficioRecebido.objects.create(
            cpf_colaborador=colaborador_instance,
            beneficio_id=beneficio_instance,
            n_condominio=condominio_instance
        )
   
        return HttpResponseRedirect(self.success_url)


# Tela Alteração dos Benefícios recebidos
class BeneficiosRecebidosUpdateViews(UpdateView):
    model = CustomBeneficioRecebido
    template_name = 'beneficios_recebidos/beneficios_recebidos_update.html'
    context_object_name = 'beneficio_recebido'
    fields = ["beneficio_id", "cpf_colaborador", "n_condominio"]
    success_url = reverse_lazy("beneficios_recebidos_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['beneficios'] = CustomBeneficio.objects.all()
        return context

    def form_valid(self, form):
        n_condominio_id = self.request.POST.get('n_condominio')

        try:
            condominio_instance = CustomCondominio.objects.get(pk=n_condominio_id)
        except CustomCondominio.DoesNotExist:
            form.add_error('n_condominio', 'Condomínio não cadastrado')
            return self.form_invalid(form)
        
        form.instance.n_condominio = condominio_instance
        return super().form_valid(form)


# Tela Exclusão dos Benefícios recebidos
class BeneficiosRecebidosDeleteViews(DeleteView):
    model = CustomBeneficioRecebido
    success_url = reverse_lazy("beneficios_recebidos_list")

    

#-----------------------Views Correspondências .................................................................

# Tela Lista as Correspondencias por Bloco e Unidade
class CorrespondenciasListViews(ListView):
    model = CustomCorrespondencia
    context_object_name = 'correspondencias_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['correspondencias'] = CustomCorrespondencia.objects.all()
        return context    
     

# Tela Cadastra as Correspondencias por Bloco e Unidade
class CorrespondenciasCreateViews(View):
    template_name = 'correspondencias/correspondencias_create.html'
    success_url = reverse_lazy("correspondencias_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['blocos'] = CustomBloco.objects.all()
        context['unidades'] = CustomUnidade.objects.all()
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        bloco_id = request.POST.get('bloco_id')
        unidade_id = request.POST.get('unidade_id')
        dsc_correspondencia = request.POST.get('dsc_correspondencia')
        data_recebimento_correspondencia = request.POST.get('data_recebimento_correspondencia')
        data_retirada_correspondencia = request.POST.get('data_retirada_correspondencia') or None
        retirante_correspondencia = request.POST.get('retirante_correspondencia')
        n_condominio = request.POST.get('n_condominio')

        if data_retirada_correspondencia == '':
            data_retirada_correspondencia = None

        try:
            CustomCorrespondencia.objects.create(
                bloco_id=CustomBloco.objects.get(bloco_id=bloco_id),
                unidade_id=CustomUnidade.objects.get(unidade_id=unidade_id),
                dsc_correspondencia=dsc_correspondencia,
                data_recebimento_correspondencia=data_recebimento_correspondencia,
                data_retirada_correspondencia=data_retirada_correspondencia,
                retirante_correspondencia=retirante_correspondencia,
                n_condominio=CustomCondominio.objects.get(n_condominio=n_condominio)
            )
            return redirect(self.success_url)
        except Exception as e:
            context = self.get_context_data()
            context['error'] = str(e)
            return render(request, self.template_name, context)


# Tela Alteração das Correspondencias por Bloco e Unidade
class CorrespondenciasUpdateViews(UpdateView):
    model = CustomCorrespondencia
    template_name = 'correspondencias/correspondencias_update.html'
    context_object_name = 'correspondencia'
    fields = [
        "data_recebimento_correspondencia", "dsc_correspondencia", "data_retirada_correspondencia", 
        "retirante_correspondencia", "bloco_id", "unidade_id", "n_condominio"
    ]
    success_url = reverse_lazy("correspondencias_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['blocos'] = CustomBloco.objects.all()
        context['unidades'] = CustomUnidade.objects.all()
        return context

    def form_valid(self, form):
        data_recebimento = form.cleaned_data.get('data_recebimento_correspondencia')
        data_retirada = form.cleaned_data.get('data_retirada_correspondencia')

        if data_retirada and data_recebimento and data_retirada <= data_recebimento:
            messages.error(self.request, 'Data de entrega da correspondência deve ser posterior a do recebimento')
            return self.form_invalid(form)

        condominio_instance = form.cleaned_data.get('n_condominio')
        bloco_instance = form.cleaned_data.get('bloco_id')
        unidade_instance = form.cleaned_data.get('unidade_id')

        if not CustomCondominio.objects.filter(n_condominio=condominio_instance.n_condominio).exists():
            messages.error(self.request, 'Número de condomínio inválido.')
            return self.form_invalid(form)
        
        if not CustomBloco.objects.filter(bloco_id=bloco_instance.bloco_id).exists():
            messages.error(self.request, 'Bloco inexistente')
            return self.form_invalid(form)
        
        if not CustomUnidade.objects.filter(unidade_id=unidade_instance.unidade_id).exists():
            messages.error(self.request, 'Unidade inexistente')
            return self.form_invalid(form)

        return super().form_valid(form)

    

# Tela Exclusão das Correspondencias por Bloco e Unidade
class CorrespondenciasDeleteViews(DeleteView):
    model = CustomCorrespondencia
    success_url = reverse_lazy("correspondencias_list")



#-----------------------Views Espaços Administrativos .................................................................

# Tela Lista os Espaços adm
class EspacosAdmListViews(ListView):
    model = CustomEspacoAdm
    context_object_name = 'espacosAdm_list'
    template_name = "espacosAdm/espacosAdm_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['espacosAdm_list'] = CustomEspacoAdm.objects.all()
        return context


# Tela Cadastro dos Espaços Adm
class EspacosAdmCreateViews(View):
    template_name = 'espacosAdm/espacosAdm_create.html'
    success_url = reverse_lazy("espacosAdm_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        nome_espaco_adm = request.POST.get('espacoAdm')
        condominio_id = request.POST.get('n_condominio')

        context = self.get_context_data()

        try:
            condominio_instance = CustomCondominio.objects.get(pk=condominio_id)
        except CustomCondominio.DoesNotExist:
            context['error'] = "Condomínio não encontrado"
            return render(request, self.template_name, context)

        CustomEspacoAdm.objects.create(
            nome_espaco_adm=nome_espaco_adm,
            n_condominio=condominio_instance,
        )
        return HttpResponseRedirect(self.success_url)


# Tela Alteração de Espaços Adm
class EspacosAdmUpdateViews(UpdateView):
    model = CustomEspacoAdm
    template_name = 'espacosAdm/espacosAdm_update.html'
    context_object_name = 'espaco_adm'
    fields = ["nome_espaco_adm", "n_condominio"]
    success_url = reverse_lazy("espacosAdm_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def form_valid(self, form):
        n_condominio_id = self.request.POST.get('n_condominio')
        if n_condominio_id:
            try:
                condominio_instance = CustomCondominio.objects.get(pk=n_condominio_id)
                form.instance.n_condominio = condominio_instance
            except CustomCondominio.DoesNotExist:
                messages.error(self.request, 'Número de condomínio inválido.')
                return self.form_invalid(form)
        return super().form_valid(form)   
    

# Tela Exclusão de Espaços Adm
class EspacosAdmDeleteViews(DeleteView):
    model = CustomEspacoAdm
    success_url = reverse_lazy("espacosAdm_list")


#-----------------------Views Tipos DE Patrimônio .................................................................

# Tela Lista os Tipos Patrimônio
class TiposPatrimonioListViews(ListView):
    model = CustomTipoPatrimonio
    context_object_name = 'tiposPatrimonio_list'
    template_name = "tiposPatrimonio/tiposPatrimonio_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tiposPatrimonio_list'] = CustomTipoPatrimonio.objects.all()
        return context


# Tela Cadastro dos Tipos Patrimônio
class TiposPatrimonioCreateViews(View):
    template_name = 'tiposPatrimonio/tiposPatrimonio_create.html'
    success_url = reverse_lazy("tiposPatrimonio_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        nome_patrimonio = request.POST.get('nome_patrimonio')
        n_patrimonio = request.POST.get('n_patrimonio')
        cor_patrimonio = request.POST.get('cor_patrimonio')
        descricao_patrimonio = request.POST.get('descricao_patrimonio')   
        condominio_id = request.POST.get('n_condominio')

        context = self.get_context_data()

        try:
            condominio_instance = CustomCondominio.objects.get(pk=condominio_id)
        except CustomCondominio.DoesNotExist:
            context['error'] = "Condomínio não encontrado"
            return render(request, self.template_name, context)

        CustomTipoPatrimonio.objects.create(
            nome_patrimonio = nome_patrimonio,
            n_patrimonio = n_patrimonio,
            cor_patrimonio = cor_patrimonio,
            descricao_patrimonio = descricao_patrimonio,
            n_condominio=condominio_instance,
        )
        return HttpResponseRedirect(self.success_url)


# Tela Alteração dos Tipos Patrimônio
class TiposPatrimonioUpdateViews(UpdateView):
    model = CustomTipoPatrimonio
    template_name = 'tiposPatrimonio/tiposPatrimonio_update.html'
    context_object_name = 'tipo_patrimonio'
    fields = ["nome_patrimonio", "n_patrimonio", "cor_patrimonio","descricao_patrimonio", "n_condominio"]
    success_url = reverse_lazy("tiposPatrimonio_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def form_valid(self, form):
        n_condominio_id = self.request.POST.get('n_condominio')
        if n_condominio_id:
            try:
                condominio_instance = CustomCondominio.objects.get(pk=n_condominio_id)
                form.instance.n_condominio = condominio_instance
            except CustomCondominio.DoesNotExist:
                messages.error(self.request, 'Número de condomínio inválido.')
                return self.form_invalid(form)
        return super().form_valid(form)   
    

# Tela Exclusão dos Tipos Patrimônio
class TiposPatrimonioDeleteViews(DeleteView):
    model = CustomTipoPatrimonio
    success_url = reverse_lazy("tiposPatrimonio_list")



#-----------------------Views DE Patrimônio .................................................................

# Tela Lista de Patrimônios
class PatrimonioListViews(ListView):
    model = CustomPatrimonio
    context_object_name = 'patrimonio_list'
    template_name = "patrimonio/patrimonio_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patrimonio_list'] = CustomPatrimonio.objects.all()
        return context


# Tela Cadastro de Patrimônio
class PatrimonioCreateViews(View):
    template_name = 'patrimonio/patrimonio_create.html'
    success_url = reverse_lazy("patrimonio_list")

    def get_context_data(self, **kwargs):
        context = {}
        context['condominios'] = CustomCondominio.objects.all()
        context['espacos'] = CustomEspacoAdm.objects.all()
        context['tiposPatrimonio'] = CustomTipoPatrimonio.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form_data'] = {
            'tipo_patrimonio_id': '',
            'espaco_adm_id': '',
            'valor_patrimonio': '',
            'data_disposicao_patrimonio': '',
            'data_baixa_patrimonio': '',
            'n_condominio': ''
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        tipo_patrimonio_id = request.POST.get('tipo_patrimonio_id')
        espaco_adm_id = request.POST.get('espaco_adm_id')
        valor_patrimonio = request.POST.get('valor_patrimonio')
        data_disposicao_patrimonio = request.POST.get('data_disposicao_patrimonio')
        data_baixa_patrimonio = request.POST.get('data_baixa_patrimonio')
        condominio_id = request.POST.get('n_condominio')

        context = self.get_context_data()

        form_data = {
            'tipo_patrimonio_id': tipo_patrimonio_id,
            'espaco_adm_id': espaco_adm_id,
            'valor_patrimonio': valor_patrimonio,
            'data_disposicao_patrimonio': data_disposicao_patrimonio,
            'data_baixa_patrimonio': data_baixa_patrimonio,
            'n_condominio': condominio_id
        }
        context['form_data'] = form_data

        # Verifica se os IDs selecionados existem no banco de dados
        try:
            condominio_instance = CustomCondominio.objects.get(pk=condominio_id)
            tipo_patrimonio_instance = CustomTipoPatrimonio.objects.get(pk=tipo_patrimonio_id)
            espaco_adm_instance = CustomEspacoAdm.objects.get(pk=espaco_adm_id)
        except CustomCondominio.DoesNotExist:
            context['error'] = "Condomínio não encontrado"
            return render(request, self.template_name, context)
        except CustomTipoPatrimonio.DoesNotExist:
            context['error'] = "Tipo de patrimônio não encontrado"
            return render(request, self.template_name, context)
        except CustomEspacoAdm.DoesNotExist:
            context['error'] = "Espaço administrativo não encontrado"
            return render(request, self.template_name, context)
        except Exception as e:
            context['error'] = f"Erro inesperado: {str(e)}"
            return render(request, self.template_name, context)

        # Verifica se data_baixa_patrimonio está vazio e atribui None se necessário
        if not data_baixa_patrimonio:
            data_baixa_patrimonio = None

        # Valida se data_baixa_patrimonio é maior que data_disposicao_patrimonio
        if data_baixa_patrimonio:
            if data_disposicao_patrimonio >= data_baixa_patrimonio:
                context['error'] = "A data de baixa deve ser superior à data de alocação"
                return render(request, self.template_name, context)

        CustomPatrimonio.objects.create(
            tipo_patrimonio_id=tipo_patrimonio_instance,
            espaco_adm_id=espaco_adm_instance,
            valor_patrimonio=valor_patrimonio,
            data_disposicao_patrimonio=data_disposicao_patrimonio,
            data_baixa_patrimonio=data_baixa_patrimonio,
            n_condominio=condominio_instance,
        )
        return HttpResponseRedirect(self.success_url)


# Tela Alteração de Patrimônio
class PatrimonioUpdateViews(UpdateView):
    model = CustomPatrimonio
    template_name = 'patrimonio/patrimonio_update.html'
    context_object_name = 'patrimonio'
    fields = ["tipo_patrimonio_id", "espaco_adm_id", "valor_patrimonio", "data_disposicao_patrimonio", "data_baixa_patrimonio", "n_condominio"]
    success_url = reverse_lazy("patrimonio_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['espacos'] = CustomEspacoAdm.objects.all()
        context['tiposPatrimonio'] = CustomTipoPatrimonio.objects.all()

        # Formatando as datas para o formato dd/mm/aa
        if self.object.data_disposicao_patrimonio:
            context['data_disposicao_patrimonio_formatada'] = DateFormat(self.object.data_disposicao_patrimonio).format(get_format('DATE_FORMAT'))
        if self.object.data_baixa_patrimonio:
            context['data_baixa_patrimonio_formatada'] = DateFormat(self.object.data_baixa_patrimonio).format(get_format('DATE_FORMAT'))

        # Formatando o valor do patrimônio para moeda brasileira
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        context['valor_patrimonio_formatado'] = f"{self.object.valor_patrimonio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        return context

    def form_valid(self, form):
        try:
            condominio_id = self.request.POST.get('n_condominio')
            tipo_patrimonio_id = self.request.POST.get('tipo_patrimonio_id')
            espaco_adm_id = self.request.POST.get('espaco_adm_id')

            if condominio_id:
                form.instance.n_condominio = CustomCondominio.objects.get(pk=condominio_id)
            if tipo_patrimonio_id:
                form.instance.tipo_patrimonio_id = CustomTipoPatrimonio.objects.get(pk=tipo_patrimonio_id)
            if espaco_adm_id:
                form.instance.espaco_adm_id = CustomEspacoAdm.objects.get(pk=espaco_adm_id)

        except CustomCondominio.DoesNotExist:
            messages.error(self.request, 'Número de condomínio inválido.')
            return self.form_invalid(form)

        except CustomEspacoAdm.DoesNotExist:
            messages.error(self.request, 'Espaço inválido.')
            return self.form_invalid(form)

        except CustomTipoPatrimonio.DoesNotExist:
            messages.error(self.request, 'Tipo de patrimônio inválido.')
            return self.form_invalid(form)
        
        # Extrai as datas do formulário
        data_disposicao_patrimonio = form.cleaned_data.get('data_disposicao_patrimonio')
        data_baixa_patrimonio = form.cleaned_data.get('data_baixa_patrimonio')

        # Verifica se data_baixa_patrimonio está vazio e atribui None se necessário
        if not data_baixa_patrimonio:
            data_baixa_patrimonio = None

        # Valida se data_baixa_patrimonio é maior que data_disposicao_patrimonio
        if data_baixa_patrimonio:
            if data_disposicao_patrimonio >= data_baixa_patrimonio:
                context = self.get_context_data()
                context['error'] = "A data de baixa deve ser superior à data de alocação"
                return self.render_to_response(context)

        return super().form_valid(form)



    

# Tela Exclusão de Patrimônio
class PatrimonioDeleteViews(DeleteView):
    model = CustomPatrimonio
    success_url = reverse_lazy("patrimonio_list")








#----------------------- SUBSISTEMA FINANCEIRO .......................................................


#-----------------------Views Plano de Contas.......................................................
        
# Tela Lista a Estrutura Plano Contas 
class FinanceiroEstruturaListViews(ListView):
    model = FinanceiroEstrutura
    context_object_name = 'financeiro_estrutura_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        financeiro_estrutura_list = FinanceiroEstrutura.objects.all()

        # Ordenar as categorias baseando-se em sua posição na hierarquia
        def sort_key(fel):
            return [int(n) for n in fel.get_nivel().split('.') if n]

        sorted_list = sorted(financeiro_estrutura_list, key=sort_key)

        # Adicionar padding baseado no nível
        for fel in sorted_list:
            nivel_count = len(fel.get_nivel().split('.'))
            fel.padding_left = nivel_count * 20  # Ajuste o valor conforme necessário

        context['financeiro_estrutura_list'] = sorted_list
        
        return context

        
    
    
# Tela Cadastro de Plano de contas
class FinanceiroEstruturaCreateViews(CreateView):
    model = FinanceiroEstrutura
    fields = ['nome', 'parent', 'n_condominio']
    template_name = 'financeiro_estrutura_form.html'
    success_url = reverse_lazy('financeiro_estrutura_list')
    widgets = {
            'n_condominio': forms.Select(choices=[(condominio.n_condominio, condominio.nome_condominio) for condominio in CustomCondominio.objects.all()]),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = FinanceiroEstrutura.objects.all()  # Show all categories
        context['condominios'] = CustomCondominio.objects.all()
        return context

    def form_valid(self, form):
        # Get the condominium object from the form
        condominio_instance = form.cleaned_data.get('n_condominio')
        
        if condominio_instance:
            # Get the condominium number from the object
            condominio_number = condominio_instance.n_condominio
            
            # Ensure that a CustomCondominio with this number exists
            if not CustomCondominio.objects.filter(n_condominio=condominio_number).exists():
                messages.error(self.request, 'Número de condomínio inválido.')
                return self.form_invalid(form)
        else:
            messages.error(self.request, 'Número de condomínio não fornecido.')
            return self.form_invalid(form)
        
        return super().form_valid(form)

       
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    
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

    def form_valid(self, form):
        # Opcionalmente, se necessário, você pode definir o 'n_condominio' aqui
        # por exemplo, para um valor padrão ou baseado em algum contexto
        form.instance.n_condominio = self.get_object().n_condominio  # Mantém o valor existente
        return super().form_valid(form)
    
# Tela Exclusão De Condôminos
class FinanceiroEstruturaDeleteViews(DeleteView):
    model = FinanceiroEstrutura
    success_url = reverse_lazy("financeiro_estrutura_list")
    
    
    
    
    
# Tela Lista as Contas a Receber
class ReceitaListViews(ListView):
    model = Receita
    context_object_name = 'receita_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['receita_list'] = Receita.objects.all()
        return context    
    
    
class ReceitaCreateViews(CreateView):
    model = Receita
    fields = [
        "data_vencimento", "data_recebimento", "numero_documento", "tipo_documento",
        "descricao", "valor", "valor_recebido", "categoria", "n_condominio"
    ]
    success_url = reverse_lazy("receita_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        # Filter categories that are at least at the 3rd level of hierarchy
        context['categorias'] = [categoria for categoria in FinanceiroEstrutura.objects.all() if len(categoria.get_nivel().split('.')) >= 3]
        return context

    def form_valid(self, form):
        # Optionally print form details for debugging
        print("Form is valid!")
        print("Form cleaned data:", form.cleaned_data)
        print("n_condominio value:", form.cleaned_data.get('n_condominio'))
        
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid!")
        print(form.errors)
        return super().form_invalid(form)


# Tela Alteração de Contas a Receber
class ReceitaUpdateViews(UpdateView):
    model = Receita
    context_object_name = 'conta_receber'
    fields = [
        "data_vencimento", "numero_documento", "tipo_documento",
        "descricao", "valor", "valor_recebido", "categoria", "n_condominio"
    ]
    success_url = reverse_lazy("receita_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['categorias'] = [categoria for categoria in FinanceiroEstrutura.objects.all() if len(categoria.get_nivel().split('.')) >= 3]
        return context

    def form_valid(self, form):
        return super().form_valid(form)

# Tela Exclusão de Contas a Receber
class ReceitaDeleteViews(DeleteView):
    model = Receita
    success_url = reverse_lazy("receita_list")



# Tela Lista as Contas a Receber
class DespesasListViews(ListView):
    model = Despesas
    context_object_name = 'despesas_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['despesas_list'] = Despesas.objects.all()
        return context    
    
    
class DespesasCreateViews(CreateView):
    model = Despesas
    fields = [
        "data_vencimento", "data_pagamento", "numero_documento", "tipo_documento",
        "descricao", "valor", "valor_pago", "categoria", "documento", "n_condominio"
    ]
    success_url = reverse_lazy("despesas_list")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['categorias'] = [categoria for categoria in FinanceiroEstrutura.objects.all() if len(categoria.get_nivel().split('.')) >= 3]
        return context

    def form_valid(self, form):
        # Optionally print form details for debugging
        print("Form is valid!")
        print("Form cleaned data:", form.cleaned_data)
        print("n_condominio value:", form.cleaned_data.get('n_condominio'))
        
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid!")
        print(form.errors)
        return super().form_invalid(form)


# Tela Alteração de Contas a Receber
class DespesasUpdateViews(UpdateView):
    model = Despesas
    context_object_name = 'conta_receber'
    fields = [
        "data_vencimento", "data_pagamento",  "numero_documento", "tipo_documento",
        "descricao", "valor", "valor_pago", "categoria", "documento", "n_condominio"
    ]
    success_url = reverse_lazy("despesas_list")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        context['categorias'] = [categoria for categoria in FinanceiroEstrutura.objects.all() if len(categoria.get_nivel().split('.')) >= 3]
        return context

    def form_valid(self, form):
        return super().form_valid(form)

# Tela Exclusão de Contas a Receber
class DespesasDeleteViews(DeleteView):
    model = Despesas
    success_url = reverse_lazy("despesas_list")
