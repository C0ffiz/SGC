from django.shortcuts import render
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

# Print('Passei POST linha 15')
# Print(novo_usuario)
