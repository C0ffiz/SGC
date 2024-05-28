# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login
# # from .models import Usuario 
# # from django.contrib.auth.hashers import make_password
# from .models import CustomUser,CustomCondomino
# from django.contrib import messages


# from django.views.generic import ListView,CreateView,UpdateView,DeleteView
# from django.urls import reverse_lazy



# #  Views Login

# def exibirLogin(request):
#     return render(request,'login/login.html')

# def verificarLogin(request):
# # verifica se as informações digitadas no login conferem com as informações na tabela usuários
#     if request.method == 'POST':
#         usuario = request.POST['usuario']
#         senha = request.POST['senha']       
       
#         user = authenticate(username=usuario,password=senha)
        
#         if user is not None:            
#             login(request, user)
#             messages.info(request, f"{usuario}")
#             return render(request, 'login/home.html')
#         else:            
#             messages.error(request, 'USUÁRIO OU SENHA INVÁLIDO')
#             return redirect('exibirLogin')
            

# def inserirUsuario(request):
#     if request.method == 'POST':
#         usuario = request.POST['usuario']
#         senha = request.POST['senha']
#         user=CustomUser.objects.create_user(username=usuario, password=senha)
#         user.save()

# #  Views Usuário

# class UsuariosListViews(ListView):
#     model = CustomUser
#     context_object_name = 'usuarios_list'

# class UsuariosCreateViews(CreateView):
#     model = CustomUser
#     fields = ["username", "password", "cpf_usuario", "nivel", "Condominio_numero"]
#     data= print("data : ")
#     success_url = reverse_lazy("usuarios_list")

# class UsuariosUpdateViews(UpdateView):
#     model = CustomUser
#     fields = ["username", "password", "cpf_usuario", "nivel", "Condominio_numero"]
#     success_url = reverse_lazy("usuarios_list")

# class UsuariosDeleteViews(DeleteView):
#     model = CustomUser
#     success_url = reverse_lazy("usuarios_list")



# #  Views Condômino

# class CondominosListViews(ListView):
#     model = CustomCondomino
#     context_object_name = 'condominos_list'

# class CondominosCreateViews(CreateView):
#     model = CustomCondomino
#     fields = ["cpf_condomino", "nome_condomino", "bloco", "apartamento", "telefone_condomino", "celular_condomino", "email_condomino", "data_aquisicao_imovel", "Condominio_numero"]
#     data= print("data : ")
#     success_url = reverse_lazy("condominos_list")

# class CondominosUpdateViews(UpdateView):
#     model = CustomCondomino
#     fields = ["cpf_condomino", "nome_condomino", "bloco", "apartamento", "telefone_condomino", "celular_condomino", "email_condomino", "data_aquisicao_imovel", "Condominio_numero"]
#     success_url = reverse_lazy("condominos_list")

# class CondominosDeleteViews(DeleteView):
#     model = CustomCondomino
#     success_url = reverse_lazy("condominos_list")

