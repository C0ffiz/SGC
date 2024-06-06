from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator

#  Definição da Tabela usuário
class CustomUser(AbstractUser):
    username = models.CharField(primary_key=True, max_length=30, null=False, blank=False)
    password = models.CharField(max_length=15, null=False, blank=False)
    cpf_usuario = models.CharField(max_length=14, validators=[MinLengthValidator(11), MaxLengthValidator(14)], null=False, blank=False)
    nivel = models.IntegerField(null=False, blank=False)
    condominio_numero = models.IntegerField(null=False, blank=False)
    class Meta:
        db_table='usuario'
        managed = True
    # def get_absolute_url(self):
    #     return reverse('usuarios_list', kwargs={'pk':self.pk})

#  Definição da Tabela Condômino
class CustomCondomino(models.Model):
    cpf_condomino = models.BigIntegerField(verbose_name="CPF Condômino *", primary_key=True, null=False, blank=False) 
    nome_condomino = models.CharField(verbose_name="Nome Condômino *",max_length=40, null=False, blank=False)
    bloco = models.CharField(verbose_name="Bloco *",max_length=2, null=False, blank=False)
    apartamento = models.CharField(verbose_name="Apartamento *",max_length=4, null=False, blank=False)
    telefone_condomino = models.CharField(verbose_name="Telefone",max_length=9, null=True, blank=True)
    celular_condomino = models.CharField(verbose_name="Celular",max_length=11, null=True, blank=True)
    email_condomino = models.CharField(verbose_name="Email",max_length=40, null=True, blank=True)
    data_aquisicao_imovel = models.DateField(verbose_name="Data aquisição imóvel *", null=False, blank=False)
    condominio_numero = models.IntegerField(null=False, blank=False)
    class Meta:
        db_table='condomino'
        managed = True
    