from django.db import models

class Usuario(models.Model):
    username = models.CharField(primary_key=True, max_length=30, null=False, blank=False)
    password = models.CharField(max_length=10, null=False, blank=False)
    cpf_usuario = models.IntegerField(null=True, blank=True)
    nivel = models.CharField(max_length=2, null=True, blank=True)
    condominio_numero = models.IntegerField(null=False, blank=False)

class Condomino(models.Model):
    cpf_condomino = models.IntegerField(verbose_name="CPF Condômino *", primary_key=True, null=False, blank=False) 
    nome_condomino = models.CharField(verbose_name="Nome Condômino *",max_length=40, null=False, blank=False)
    bloco = models.CharField(verbose_name="Bloco *",max_length=2, null=False, blank=False)
    apartamento = models.CharField(verbose_name="Apartamento *",max_length=4, null=False, blank=False)
    telefone = models.CharField(verbose_name="Telefone",max_length=9, null=True, blank=True)
    celular = models.CharField(verbose_name="Celular",max_length=11, null=True, blank=True)
    email = models.CharField(verbose_name="Email",max_length=40, null=True, blank=True)
    data_aquisicao_imovel = models.DateField(verbose_name="Data aquisição imóvel *", null=False, blank=False)
    Condominio_numero = models.IntegerField(null=False, blank=False)
