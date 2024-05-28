from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
# from .models import Usuario 
# from django.contrib.auth.hashers import make_password
from .models import CustomUser,CustomCondomino
from django.contrib import messages


from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy



#  Views Login

def exibirLogin(request):
    return render(request,'login/login.html')

def verificarLogin(request):
# verifica se as informações digitadas no login conferem com as informações na tabela usuários
    if request.method == 'POST':
        usuario = request.POST['usuario']
        senha = request.POST['senha']       
       
        user = authenticate(username=usuario,password=senha)
        
        if user is not None:            
            login(request, user)
            messages.info(request, f"{usuario}")
            return render(request, 'login/home.html')
        else:            
            messages.error(request, 'USUÁRIO OU SENHA INVÁLIDO')
            return redirect('exibirLogin')
            

def exibirHome(request):
    return render(request,'login/home.html')



# def inserirUsuario(request):
#     if request.method == 'POST':
#         usuario = request.POST['usuario']
#         senha = request.POST['senha']
#         user=CustomUser.objects.create_user(username=usuario, password=senha)
#         user.save()

#  Views Usuário

class UsuariosListViews(ListView):
    model = CustomUser
    context_object_name = 'usuarios_list'

class UsuariosCreateViews(CreateView):
    model = CustomUser
    template_name = 'usuarios_create.html'
    fields = ["username", "password", "cpf_usuario", "nivel", "condominio_numero"]
    success_url = reverse_lazy("usuarios_list")

    # def form_valid(self, form):
    #     # Antes de salvar o formulário, atribuímos a senha corretamente.
    #     # O atributo 'password' no modelo CustomUser não é usado diretamente para armazenar a senha criptografada.
    #     # O Django cuida disso internamente.
    #     form.instance.set_password(form.cleaned_data['password'])

    #     # Chama o método da classe pai para salvar o formulário.
    #     return super().form_valid(form)

class UsuariosUpdateViews(UpdateView):
    model = CustomUser
    # template_name = 'usuarios_update.html'
    fields = ["username", "password", "cpf_usuario", "nivel", "condominio_numero"]
    success_url = reverse_lazy("usuarios_list")

class UsuariosDeleteViews(DeleteView):
    model = CustomUser
    success_url = reverse_lazy("usuarios_list")



#  Views Condômino

class CondominosListViews(ListView):
    model = CustomCondomino
    context_object_name = 'condominos_list'

class CondominosCreateViews(CreateView):
    model = CustomCondomino
    fields = ["cpf_condomino", "nome_condomino", "bloco", "apartamento", "telefone_condomino", "celular_condomino", "email_condomino", "data_aquisicao_imovel", "Condominio_numero"]
    data= print("data : ")
    success_url = reverse_lazy("condominos_list")

class CondominosUpdateViews(UpdateView):
    model = CustomCondomino
    fields = ["cpf_condomino", "nome_condomino", "bloco", "apartamento", "telefone_condomino", "celular_condomino", "email_condomino", "data_aquisicao_imovel", "Condominio_numero"]
    success_url = reverse_lazy("condominos_list")

class CondominosDeleteViews(DeleteView):
    model = CustomCondomino
    success_url = reverse_lazy("condominos_list")

