from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Usuario
from django.contrib.auth.hashers import make_password

def login(request):
    return render(request,'login/login.html')

def register(request):
    return render(request, 'login/register.html')

def realizaRegistro(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['senha']
        cpf = request.POST['cpf']
        nivel = request.POST['nivel']
        condominio = request.POST['condominio']
    
        user = User.objects.create_user(username, password)
        user.cpf = cpf
        user.nivel = nivel
        user.condominio = condominio
        user.save()
        
        return redirect('login')
    
    return render(request, "login/register.html")
#
def usuarios(request):
# Busca as informações digitadas na tela
    novo_usuario = Usuario()
    novo_usuario.usuario = request.POST.get('usuario')
    novo_usuario.senha = request.POST.get('senha')
    novo_usuario.cpf_usuario = 22760369153
    novo_usuario.nivel = 1

def verificaLogin(request):
# verifica se as informações digitadas no login conferem com as informações na tabela usuários
    if request.method == 'POST':
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        user = authenticate(username=usuario,password=senha)

        print(user)
        
        
        

        print(usuario,senha)

        if user is not None:
            print('Usuário Válido *************************************')
        else:
            print('Usuário Inválido ***********************************')
            

