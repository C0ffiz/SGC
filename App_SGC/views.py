from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import CustomUser,CustomCondominio,CustomCondomino,CustomCondominio,CustomMorador
from django.contrib import messages
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy, reverse
from django import forms


#-----------------------Views Login

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
                messages.info(request, f"{usuario}")
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


#-----------------------Views Usuário

# Tela Usuarios
class UsuariosListViews(ListView):
    model = CustomUser
    context_object_name = 'usuarios_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['condominios'] = CustomCondominio.objects.all()
        return context

# Tela Cadastro De Usuarios
class UsuariosCreateViews(CreateView):
    model = CustomUser
    template_name = 'usuarios_create.html'
    fields = ["username", "password", "cpf_usuario", "nivel", "n_condominio"]
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
    fields = ["username", "password", "cpf_usuario", "nivel", "n_condominio"]
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
    

#-----------------------Views Condômino

class CondominosListViews(ListView):
    model = CustomCondomino
    context_object_name = 'condominos_list'


class CondominosCreateViews(CreateView):
    model = CustomCondomino
    fields = ["cpf_condomino", "nome_condomino", "bloco", "apartamento", "telefone_condomino", "celular_condomino", "email_condomino", "data_aquisicao_imovel", "data_nascimento_condomino", "n_condominio"]
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
    

# Tela Alteração De Condominos
class CondominosUpdateViews(UpdateView):
    model = CustomCondomino
    context_object_name = 'condominos_list'    
    fields = ["cpf_condomino", "nome_condomino", "data_nascimento_condomino", "bloco", "apartamento", "telefone_condomino", "celular_condomino", "email_condomino", "data_aquisicao_imovel", "n_condominio"]
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
    
# Tela Exclusão De Condominos
class CondominosDeleteViews(DeleteView):
    model = CustomCondomino
    success_url = reverse_lazy("condominos_list")


#-----------------------Views Condomínios

# Tela Condomínios
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
    

#-----------------------Views Moradores

# Tela Moradores
class MoradoresListViews(ListView):
    model = CustomMorador
    context_object_name = 'moradores_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['moradores'] = CustomMorador.objects.all()
        return context

# Tela Verificar Moradores
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
            print("ERROR 1 ######################################")
            return self.form_invalid(form)
        
        # Verifica se o CPF do condômino já está cadastrado
        condomino = CustomCondomino.objects.filter(cpf_condomino=cpf_condomino_str).first()
        print("Queryset result:", condomino)
        if not condomino:
            messages.error(self.request, 'CPF de condômino não encontrado.')
            print("ERROR 2 ######################################")
            return self.form_invalid(form)
            
        # Assign the condomínio to the morador
        form.instance.cpf_condomino = condomino
        form.instance.n_condominio = condomino.n_condominio

        self.object = form.save()
        print("passou ######################################")
        
        # Recarrega página com o mesmo cpf
        return redirect(reverse('moradores_create') + f'?cpf_condomino={cpf_condomino_str}')
    

    def form_invalid(self, form):
        print("NNNNNNNNN passou ######################################")
        return super().form_invalid(form)
    
    

# Tela Alteração De Moradores
class MoradoresUpdateViews(UpdateView):
    model = CustomMorador
    # context_object_name = 'usuarios_list'
    # fields = ["username", "password", "cpf_usuario", "nivel", "n_condominio"]
    # success_url = reverse_lazy("usuarios_list") 
    # widgets = {
    #     'n_condominio': forms.Select(attrs={'class': 'form-control'}),
    # }
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['condominios'] = CustomCondominio.objects.all()
#         return context
    
    # def form_valid(self, form):
        # Strip mask from CPF
        # cpf_usuario = form.cleaned_data['cpf_usuario'].replace(".", "").replace("-", "")
        # form.instance.cpf_usuario = cpf_usuario
        
        # Get the selected condominium instance
        # condominio_instance = form.cleaned_data['n_condominio']

        # Assign the primary key of the selected condominium to the field
        # form.instance.n_condominio_id = condominio_instance.n_condominio

        # Check if the selected condominium number exists
        # if not CustomCondominio.objects.filter(n_condominio=form.instance.n_condominio_id).exists():
        #     messages.error(self.request, 'Número de condomínio inválido.')
        #     return self.form_invalid(form)
        
        # return super().form_valid(form)
    

# Tela Exclusão De Usuarios
class MoradoresDeleteViews(DeleteView):
    model = CustomMorador
    success_url = reverse_lazy("moradores_list")
