from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import CustomUser,CustomCondomino
from django.contrib import messages
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy


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

# Tela Cadastro De Usuarios
class UsuariosCreateViews(CreateView):
    model = CustomUser
    template_name = 'usuarios_create.html'
    fields = ["username", "password", "cpf_usuario", "nivel", "condominio_numero"]
    success_url = reverse_lazy("usuarios_list")
    
    def form_valid(self, form):
        # Strip mask from CPF
        cpf_usuario = form.cleaned_data['cpf_usuario'].replace(".", "").replace("-", "")
        form.instance.cpf_usuario = cpf_usuario
        return super().form_valid(form)

# Tela Alteração De Usuarios
class UsuariosUpdateViews(UpdateView):
    model = CustomUser
    context_object_name = 'usuarios_list'
    fields = ["username", "password", "cpf_usuario", "nivel", "condominio_numero"]
    success_url = reverse_lazy("usuarios_list")
    
    def form_valid(self, form):
        # Strip mask from CPF
        cpf_usuario = form.cleaned_data['cpf_usuario'].replace(".", "").replace("-", "")
        form.instance.cpf_usuario = cpf_usuario
        return super().form_valid(form)

# Tela Exclusão De Usuarios
class UsuariosDeleteViews(DeleteView):
    model = CustomUser
    success_url = reverse_lazy("usuarios_list")



#-----------------------Views Condômino

# Tela Condominos
class CondominosListViews(ListView):
    model = CustomCondomino
    context_object_name = 'condominos_list'

# Tela Cadastro De Condominos
class CondominosCreateViews(CreateView):
    model = CustomCondomino
    fields = ["cpf_condomino", "nome_condomino", "bloco", "apartamento", "telefone_condomino", "celular_condomino", "email_condomino", "data_aquisicao_imovel", "Condominio_numero"]
    data= print("data : ")
    success_url = reverse_lazy("condominos_list")

# Tela Alteração De Condominos
class CondominosUpdateViews(UpdateView):
    model = CustomCondomino
    fields = ["cpf_condomino", "nome_condomino", "bloco", "apartamento", "telefone_condomino", "celular_condomino", "email_condomino", "data_aquisicao_imovel", "Condominio_numero"]
    success_url = reverse_lazy("condominos_list")

# Tela Exclusão De Condominos
class CondominosDeleteViews(DeleteView):
    model = CustomCondomino
    success_url = reverse_lazy("condominos_list")

