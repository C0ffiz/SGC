from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
# from .models import Usuario 
from django.contrib.auth.hashers import make_password
from .models import CustomUser

def exibirLogin(request):
    return render(request,'login/login.html')

def verificarLogin(request):
# verifica se as informações digitadas no login conferem com as informações na tabela usuários
    if request.method == 'POST':
        usuario = request.POST['usuario']
        senha = request.POST['senha']
       
        print('Antes do authenti... ***********************************')
        user = authenticate(username=usuario,password=senha)

        print(usuario,senha)

        if user is not None:
            print('Usuário Válido *************************************')
            login(request, user)
            return render(request, 'login/home.html')
        else:
            print('Usuário Inválido ***********************************')
            return redirect('login')
            

def inserirUsuario(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        user=CustomUser.objects.create_user(username='teste1', password='1234')
        user.save()