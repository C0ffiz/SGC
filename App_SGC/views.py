from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import Usuario

def login(request):
    return render(request,'login/login.html')

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

        print(usuario,senha)

        if user is not None:
            print('Usuário Válido *************************************')
        else:
            print('Usuário Inválido ***********************************')
            

