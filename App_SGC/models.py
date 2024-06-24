from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator


#  Definição da Tabela usuário
class CustomUser(AbstractUser):
    username = models.CharField(primary_key=True, max_length=30, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    cpf_usuario = models.CharField(max_length=14, validators=[MinLengthValidator(11), MaxLengthValidator(14)], null=False, blank=False)
    nivel = models.IntegerField(null=False, blank=False, default=0)
    n_condominio = models.ForeignKey(
        'CustomCondominio',  
        on_delete=models.CASCADE,
        verbose_name="Número do Condomínio",
        null=False,  
        blank=False,  
        default=0)
    
    class Meta:
        db_table='usuario'
        managed = True

      
#  Definição da Tabela do Condomínio 
class CustomCondominio(models.Model):
    n_condominio = models.IntegerField(verbose_name="Número do Condomínio *", primary_key=True, default=0) 
    nome_condominio = models.CharField(verbose_name="Nome do Condomínio *", max_length=60, null=False, blank=False)
    
    class Meta:
        db_table='condominio'
        managed = True
   

#  Definição da Tabela Condômino
class CustomCondomino(models.Model):
    cpf_condomino = models.BigIntegerField(verbose_name="CPF Condômino *", primary_key=True, null=False, blank=False) 
    nome_condomino = models.CharField(verbose_name="Nome Condômino *",max_length=40, null=False, blank=False)
    data_nascimento_condomino = models.DateField(verbose_name="Data Nascimento *", null=False, blank=False, default='0000-00-00')
    bloco = models.CharField(verbose_name="Bloco *",max_length=2, null=False, blank=False)
    apartamento = models.CharField(verbose_name="Apartamento *",max_length=4, null=False, blank=False)
    telefone_condomino = models.CharField(verbose_name="Telefone",max_length=9, null=True, blank=True, default='-')
    celular_condomino = models.CharField(verbose_name="Celular",max_length=11, null=True, blank=True)
    email_condomino = models.CharField(verbose_name="E-mail",max_length=40, null=True, blank=True, default='-')
    data_aquisicao_imovel = models.DateField(verbose_name="Data Aquisição Imóvel *", null=False, blank=False, default='0000-00-00')
    n_condominio = models.ForeignKey(
        'CustomCondominio',  
        on_delete=models.CASCADE,
        verbose_name="Número do Condomínio",
        null=False,  
        blank=False,
        default=0)
        
    class Meta:
        db_table='condomino'
        managed = True


# Definição da Tabela Morador
class CustomMorador(models.Model):
    cpf_condomino = models.ForeignKey(
        'CustomCondomino', 
        on_delete=models.CASCADE, 
        verbose_name="CPF Condômino *", 
        null=False, 
        blank=False,
        related_name='moradores_por_cpf'
    )
    cpf_morador = models.BigIntegerField(verbose_name="CPF Morador *", primary_key=True, null=False, blank=False)
    nome_morador = models.CharField(verbose_name="Nome Morador *", max_length=40, null=False, blank=False)
    data_nascimento_morador = models.DateField(verbose_name="Data de Nascimento *", null=False, blank=False)
    parentesco_condomino = models.CharField(verbose_name="Parentesco", max_length=11, null=False, blank=False, default="Outros")
    celular_morador = models.CharField(verbose_name="Celular", max_length=11, null=True, blank=True)
    email_morador = models.CharField(verbose_name="Email", max_length=40, null=True, blank=True)
    n_condominio = models.ForeignKey(
        'CustomCondomino', 
        on_delete=models.CASCADE, 
        verbose_name="Número do Condomínio", 
        null=False, 
        blank=False,
        related_name='numero_condominio'
    )

    class Meta:
        db_table = 'morador'
        managed = True



#  4 Definição da Tabela Colaborador
class CustomColaborador(models.Model):   
    cpf_colaborador = models.BigIntegerField(verbose_name="CPF Colaborador *", primary_key=True, null=False, blank=False) 
    nome_colaborador = models.CharField(verbose_name="Nome Colaborador *",max_length=40, null=False, blank=False)
    data_nascimento_colaborador = models.DateField(verbose_name="Data nascimento *", null=False, blank=False)
    endereco_colaborador = models.CharField(verbose_name="Endereço *",max_length=70, null=False, blank=False)
    telefone_colaborador = models.CharField(verbose_name="Telefone",max_length=9, null=True, blank=True)
    celular_colaborador = models.CharField(verbose_name="Celular",max_length=11, null=False, blank=False)
    email_colaborador = models.CharField(verbose_name="Email",max_length=40, null=True, blank=True) 
    nome_contato_colaborador = models.CharField(verbose_name="Nome Contato *",max_length=40, null=False, blank=False)
    celular_contato_colaborador = models.CharField(verbose_name="Celular Contato",max_length=11, null=False, blank=False)
    n_condominio = models.ForeignKey(
        'CustomCondominio',  # Foreign key to CustomCondominio
        on_delete=models.CASCADE,
        verbose_name="Número Condomínio *",
        null=False,
        blank=False
    )
    
    class Meta:
        db_table='colaborador'
        managed = True


        # Definição da Tabela Nivel de acesso ao sistema
# class CustomNivel(models.Model):
#     nivel = models.IntegerField(verbose_name="Nível usuário *", primary_key=True, null=False, blank=False) 
#     n_tela = models.ForeignKey('CustomTela', verbose_name="Número tela *", on_delete=models.CASCADE)  # Adicione 'to' e 'on_delete'

#     class Meta:
#         db_table = 'nivel'
#         managed = True

    

#  7 Definição da Tabela de Telas do sistema
# class CustomTela(models.Model):
#     n_tela = models.IntegerField(verbose_name="Nº da tela *", primary_key=True) 
#     nome_tela = models.CharField(verbose_name="Nome da tela *",max_length=40, null=False, blank=False)
#     class Meta:
#         db_table='tela'
#         managed = True





