from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator
from datetime import date


# Definição da Tabela Usuário...................................................................
class CustomUser(AbstractUser):
    username = models.CharField(primary_key=True, max_length=30, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    cpf_usuario = models.CharField(max_length=14, validators=[MinLengthValidator(11), MaxLengthValidator(14)], null=False, blank=False)
    n_condominio = models.ForeignKey(
        'CustomCondominio',  
        on_delete=models.CASCADE,
        verbose_name="Número do Condomínio",
        null=False,  
        blank=False,  
        )
    
    class Meta:
        db_table='usuario'
        managed = True
        ordering = ['username']      


# Definição da Tabela Condomínio...................................................................
class CustomCondominio(models.Model):
    n_condominio = models.IntegerField(verbose_name="Número do Condomínio *", primary_key=True,) 
    nome_condominio = models.CharField(verbose_name="Nome do Condomínio *", max_length=60, null=False, blank=False)
    
    class Meta:
        db_table='condominio'
        managed = True
        ordering = ['nome_condominio']


# Definição da Tabela Condômino...................................................................
class CustomCondomino(models.Model):
    cpf_condomino = models.CharField(verbose_name="CPF Condômino *", max_length=14, primary_key=True, null=False, blank=False) 
    nome_condomino = models.CharField(verbose_name="Nome Condômino *",max_length=40, null=False, blank=False)
    data_nascimento_condomino = models.DateField(verbose_name="Data Nascimento *", null=False, blank=False, default='0000-00-00')    
    telefone_condomino = models.CharField(verbose_name="Telefone",max_length=10, null=True, blank=True, default='-')
    celular_condomino = models.CharField(verbose_name="Celular",max_length=11, null=True, blank=True)
    email_condomino = models.CharField(verbose_name="E-mail",max_length=40, null=True, blank=True, default='-')
    data_aquisicao_imovel = models.DateField(verbose_name="Data Aquisição Imóvel *", null=False, blank=False, default='0000-00-00')
    n_condominio = models.ForeignKey(
        CustomCondominio,  
        on_delete=models.CASCADE,
        verbose_name="Número do Condomínio",
        null=False,  
        blank=False,
        )
        
    class Meta:
        db_table='condomino'
        managed = True
        ordering = ['nome_condomino']


# Definição da Tabela Morador...................................................................
class CustomMorador(models.Model):
    cpf_condomino = models.ForeignKey(
        CustomCondomino, 
        on_delete=models.CASCADE, 
        verbose_name="CPF Condômino *", 
        null=False, 
        blank=False,
        related_name='moradores_por_cpf')
    cpf_morador = models.CharField(verbose_name="CPF Morador *", max_length=14, primary_key=True, null=False, blank=False)
    nome_morador = models.CharField(verbose_name="Nome Morador *", max_length=40, null=False, blank=False)
    data_nascimento_morador = models.DateField(verbose_name="Data de Nascimento *", null=False, blank=False)
    PARENTESCO_CHOICES = [
        ('esposo', 'Esposo(a)'),
        ('filho', 'Filho(a)'),
        ('pai', 'Pai'),
        ('mae', 'Mãe'),
        ('locatario', 'Locatário'),
        ('outros', 'Outros'),
    ]
    parentesco_condomino = models.CharField(
        verbose_name="Parentesco",
        max_length=11,
        choices=PARENTESCO_CHOICES,
        default='outros',  # Defina o valor padrão conforme necessário
        null=False,
        blank=False)
    celular_morador = models.CharField(verbose_name="Celular", max_length=11, null=True, blank=True)
    email_morador = models.CharField(verbose_name="Email", max_length=40, null=True, blank=True)
    n_condominio = models.ForeignKey(
        CustomCondominio, 
        on_delete=models.CASCADE, 
        verbose_name="Número do Condomínio", 
        null=False, 
        blank=False,
        related_name='numero_condominio')
    
    class Meta:
        db_table='morador'
        managed = True
        ordering = ['nome_morador']
        unique_together = ('cpf_condomino', 'cpf_morador')  


#  Definição da Tabela do Veículo...................................................................
class CustomVeiculo(models.Model):
    placa_veiculo = models.CharField(verbose_name="Placa Veículo *", primary_key=True, max_length=7, null=False, blank=False)
    marca_veiculo = models.CharField(verbose_name="Marca do Veículo *", max_length=30, null=False, blank=False)
    modelo_veiculo = models.CharField(verbose_name="Modelo do Veículo *", max_length=30, null=False, blank=False)
    cor_veiculo = models.CharField(verbose_name="Cor do Veículo *", max_length=30, null=False, blank=False)
    cpf_condomino = models.ForeignKey(
        'CustomCondomino', 
        on_delete=models.CASCADE, 
        verbose_name="CPF Condômino *", 
        null=False, 
        blank=False,
        related_name='veiculos_por_cpf')
    
    class Meta:
        db_table='veiculo'
        managed = True
        ordering = ['cpf_condomino']


#  Definição da Tabela Colaborador...................................................................
class CustomColaborador(models.Model):   
    cpf_colaborador = models.CharField(verbose_name="CPF Condômino *", max_length=14, primary_key=True, null=False, blank=False) 
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
        blank=False)
    
    class Meta:
        db_table='colaborador'
        managed = True
        ordering = ['nome_colaborador']


#  Definição da Tabela Bloco...................................................................
class CustomBloco(models.Model):
    bloco_id = models.AutoField(primary_key=True)
    bloco = models.CharField(verbose_name="Bloco *", max_length=2, null=False, blank=False)
    n_condominio = models.ForeignKey(
        CustomCondominio,  # Foreign key to CustomCondominio
        on_delete=models.CASCADE,
        verbose_name="Número Condomínio *",
        null=False,
        blank=False,
        )              
    class Meta:
        db_table = 'bloco'
        managed = True
        ordering = ['bloco']



# Definição da Tabela Unidade................................................................... 
class CustomUnidade(models.Model):
    unidade_id = models.AutoField(primary_key=True)
    unidade = models.CharField(verbose_name="Unidade *", max_length=4, null=False, blank=False)
    cpf_condomino = models.ForeignKey(
        'CustomCondomino', 
        on_delete=models.CASCADE, 
        verbose_name="CPF Condômino *", 
        null=False, 
        blank=False,
        related_name='unidade_por_cpf')
    bloco_id = models.ForeignKey(
        'CustomBloco', 
        on_delete=models.CASCADE, 
        verbose_name="Bloco *", 
        null=False, 
        blank=False,
        related_name='unidade_por_bloco')
    n_condominio = models.ForeignKey(
        'CustomCondominio',  # Foreign key to CustomCondominio
        on_delete=models.CASCADE,
        verbose_name="Número Condomínio *",
        null=False,
        blank=False)
           
    class Meta:
        db_table = 'unidade'
        managed = True
        ordering = ['bloco_id__bloco', 'unidade']


# Definição da Tabela Garagens................................................................... 
class CustomGaragem(models.Model):
    garagem_id = models.AutoField(primary_key=True)
    n_garagem = models.CharField(verbose_name="Garagem *", max_length=4, null=False, blank=False)
    cpf_condomino = models.ForeignKey(
        'CustomCondomino', 
        on_delete=models.CASCADE, 
        verbose_name="CPF Condômino *", 
        null=False, 
        blank=False,
        related_name='veiculo_por_cpf')
    bloco_id = models.ForeignKey(
        'CustomBloco', 
        on_delete=models.CASCADE, 
        verbose_name="Bloco *", 
        null=False, 
        blank=False,
        related_name='veiculo_por_bloco')
    n_condominio = models.ForeignKey(
        'CustomCondominio',  
        on_delete=models.CASCADE,
        verbose_name="Número Condomínio *",
        null=False,
        blank=False)
           
    class Meta:
        db_table = 'garagem'
        managed = True
        ordering = ['bloco_id__bloco', 'n_garagem']


# Definição da Tabela Mudanças................................................................... 
class CustomMudanca(models.Model):
    mudanca_id = models.AutoField(primary_key=True)
    data_mudanca = models.DateField(verbose_name="Data mudança *", null=False, blank=False)
    hora_mudanca = models.TimeField(verbose_name="Hora mudança *", null=False, blank=False)
    transportadora = models.CharField(verbose_name="Transportadora *", max_length=40, null=True, blank=True)
    placa_veiculo_transportadora = models.CharField(verbose_name="Placa Veículo *", max_length=7, null=True, blank=True)
    cpf_condomino = models.ForeignKey(
        'CustomCondomino', 
        on_delete=models.CASCADE, 
        verbose_name="CPF Condômino *", 
        null=False, 
        blank=False,
        related_name='mudanca_por_cpf')
    bloco_id = models.ForeignKey(
        'CustomBloco', 
        on_delete=models.CASCADE, 
        verbose_name="Bloco *", 
        null=False, 
        blank=False,
        related_name='mudanca_por_bloco')
    unidade_id = models.ForeignKey(
        'CustomUnidade', 
        on_delete=models.CASCADE, 
        verbose_name="Mudança *", 
        null=False, 
        blank=False,
        related_name='mudanca_por_unidade')
    n_condominio = models.ForeignKey(
        'CustomCondominio',  # Foreign key to CustomCondominio
        on_delete=models.CASCADE,
        verbose_name="Número Condominio *",
        null=False,
        blank=False)
               
    class Meta:
        db_table = 'mudanca'
        managed = True
        ordering = ['bloco_id__bloco', 'data_mudanca']


# Definição da Tabela Ocorrências................................................................... 
class CustomOcorrencia(models.Model):
    ocorrencia_id = models.AutoField(primary_key=True)
    data_ocorrencia = models.DateField(verbose_name="Data mudança *", null=False, blank=False)
    hora_ocorrencia = models.TimeField(verbose_name="Hora mudança *", null=False, blank=False)
    dsc_ocorrencia = models.CharField(verbose_name="Transportadora *", max_length=60, null=True, blank=True)
    documento_ocorrencia = models.FileField(upload_to='documentos_ocorrencias/', null=False, blank=False)
    cpf_condomino = models.ForeignKey(
        'CustomCondomino', 
        on_delete=models.CASCADE, 
        verbose_name="CPF Condômino *", 
        null=False, 
        blank=False,
        related_name='ocorrencia_por_cpf')
  
    n_condominio = models.ForeignKey(
        'CustomCondominio',  # Foreign key to CustomCondominio
        on_delete=models.CASCADE,
        verbose_name="Número Condominio *",
        null=False,
        blank=False)
               
    class Meta:
        db_table = 'ocorrencia'
        managed = True
        ordering = ['data_ocorrencia', 'hora_ocorrencia']


# Definição da Tabela Benefícios...............................................................................
class CustomBeneficio(models.Model):
    beneficio_id = models.AutoField(primary_key=True)
    nome_beneficio = models.CharField(verbose_name="Transportadora *", max_length=60, null=True, blank=True)    
    n_condominio = models.ForeignKey(
        'CustomCondominio',  # Foreign key to CustomCondominio
        on_delete=models.CASCADE,
        verbose_name="Número Condominio *",
        null=False,
        blank=False)
               
    class Meta:
        db_table = 'beneficio'
        managed = True
        ordering = ['nome_beneficio']


# Definição da Tabela Benefícios Recebidos................................................................... 
class CustomBeneficioRecebido(models.Model):
    beneficio_recebido_id = models.AutoField(primary_key=True)
    beneficio_id = models.ForeignKey(
        'CustomBeneficio',  
        on_delete=models.CASCADE,
        verbose_name="Benefício *",
        null=False,
        blank=False)
    cpf_colaborador = models.ForeignKey(
        'CustomColaborador', 
        on_delete=models.CASCADE, 
        verbose_name="CPF Colaborador *", 
        null=False, 
        blank=False,
        related_name='beneficio_recebido_por_colaborador')   
    n_condominio = models.ForeignKey(
        'CustomCondominio',  # Foreign key to CustomCondominio
        on_delete=models.CASCADE,
        verbose_name="Número Condominio *",
        null=False,
        blank=False)
               
    class Meta:
        db_table = 'beneficio_recebido'
        managed = True
        ordering = ['cpf_colaborador', 'beneficio_id']
        unique_together = ('beneficio_id', 'cpf_colaborador', 'n_condominio') 










#
# DEFINIÇÃO DE TABELAS DO SUBSISTEMA FINANCEIRO ........................................................
#

# Definição da Tabela Plano de Contas...................................................................
class CustomPlano_Conta(models.Model):
    nivel_1 = models.CharField(verbose_name="Nível 1 *", max_length=1, null=False, blank=False)
    nivel_2 = models.CharField(verbose_name="Nível 2 *", max_length=1, null=False, blank=False)
    nivel_3 = models.CharField(verbose_name="Nível 3 *", max_length=1, null=False, blank=False)
    nivel_4 = models.CharField(verbose_name="Nível 4 *", max_length=1, null=False, blank=False)
    dsc_plano_conta = models.CharField(verbose_name="Dsc *", max_length=100, null=False, blank=False)
    n_condominio = models.ForeignKey(
        'CustomCondominio',  # Foreign key to CustomCondominio
        on_delete=models.CASCADE,
        verbose_name="Número Condominio *",
        null=False,
        blank=False)
    
    class Meta:
        db_table = 'plano_conta'
        managed = True
        ordering = ['nivel_1', 'nivel_2', 'nivel_3', 'nivel_4']
        unique_together = (('nivel_1', 'nivel_2', 'nivel_3', 'nivel_4'),)  # Define a chave composta

    def __str__(self):
        return f"{self.nivel_1}.{self.nivel_2}.{self.nivel_3}.{self.nivel_4} - {self.dsc_plano_conta}"


# Definição da Tabela Contas a Receber...................................................................
class CustomConta_Receber(models.Model):
    data_conta_receber = models.DateField(verbose_name="Data vencimento *", null=False, blank=False)
    data_recebimento = models.DateField(verbose_name="Data recebimento *", null=True, blank=True)
    n_documento_conta_receber = models.CharField(verbose_name="Nº documento *", max_length=20, null=False, blank=False)  
    tipo_documento_conta_receber_CHOICES = [
        ('NF', 'NF'),
        ('Recibo', 'Recibo'),
        ('outros', 'Outros'),
    ]
    tipo_documento_conta_receber = models.CharField(
        verbose_name="Tipo do Documento",
        max_length=6,
        choices=tipo_documento_conta_receber_CHOICES,
        default='NF',  # Defina o valor padrão conforme necessário
        null=False,
        blank=False)
    dsc_conta_receber = models.CharField(verbose_name="Dsc *", max_length=60, null=False, blank=False)
    valor_conta_receber = models.IntegerField(verbose_name="Valor *", null=False, blank=False)
    nivel_1 = models.ForeignKey(
        'CustomPlano_Conta',  
        on_delete=models.CASCADE,
        verbose_name="Receber Nível 1 *",
        null=False,
        blank=False,
        related_name='nivel_1_por_conta_receber')
    nivel_2 = models.ForeignKey(
        'CustomPlano_Conta',  
        on_delete=models.CASCADE,
        verbose_name="Receber Nível 2 *",
        null=False,
        blank=False,
        related_name='nivel_2_por_conta_receber')
    nivel_3 = models.ForeignKey(
        'CustomPlano_Conta',  
        on_delete=models.CASCADE,
        verbose_name="Receber Nível 3 *",
        null=False,
        blank=False,
        related_name='nivel_3_por_conta_receber')
    nivel_4 = models.ForeignKey(
        'CustomPlano_Conta',  
        on_delete=models.CASCADE,
        verbose_name="Receber Nível 4 *",
        null=False,
        blank=False,
        related_name='nivel_4_por_conta_receber')    
    n_condominio = models.ForeignKey(
        'CustomCondominio',  # Foreign key to CustomCondominio
        on_delete=models.CASCADE,
        verbose_name="Número Condominio *",
        null=False,
        blank=False)
    
    class Meta:
        db_table = 'conta_receber'
        managed = True
        ordering = ['data_conta_receber', 'tipo_documento_conta_receber', 'nivel_1', 'nivel_2', 'nivel_3', 'nivel_4'] 
        unique_together = ('data_conta_receber', 'n_documento_conta_receber') # Chave composta por estas colunas 

    def __str__(self):
        return f"{self.data_conta_receber} - {self.n_documento_conta_receber} - {self.tipo_documento_conta_receber} - {self.dsc_conta_receber}"


# Definição da Tabela Contas a Pagar...................................................................
class CustomConta_Pagar(models.Model):
    data_conta_pagar = models.DateField(verbose_name="Data vencimento *", default=date.today, null=False, blank=False)
    data_pagamento = models.DateField(verbose_name="Data pagamento *", null=True, blank=True)
    n_documento_conta_pagar = models.CharField(verbose_name="Nº documento *", max_length=20, null=False, blank=False)  
    tipo_documento_conta_pagar_CHOICES = [
        ('NF', 'NF'),
        ('Recibo', 'Recibo'),
        ('outros', 'Outros'), 
    ]
    tipo_documento_conta_pagar = models.CharField(
        verbose_name="Tipo do Documento",
        max_length=6,
        choices=tipo_documento_conta_pagar_CHOICES,
        default='NF',  # Defina o valor padrão conforme necessário
        null=False,
        blank=False)
    dsc_conta_pagar = models.CharField(verbose_name="Dsc *", max_length=60, null=False, blank=False)
    valor_conta_pagar = models.IntegerField(verbose_name="Valor *", null=False, blank=False)
    nivel_1 = models.ForeignKey(
        'CustomPlano_Conta',  
        on_delete=models.CASCADE,
        verbose_name="Pagar Nível 1 *",
        null=False,
        blank=False,
        related_name='nivel_1_por_conta_pagar')
    nivel_2 = models.ForeignKey(
        'CustomPlano_Conta',  
        on_delete=models.CASCADE,
        verbose_name="Pagar Nível 2 *",
        null=False,
        blank=False,
        related_name='nivel_2_por_conta_pagar')
    nivel_3 = models.ForeignKey(
        'CustomPlano_Conta',  
        on_delete=models.CASCADE,
        verbose_name="Pagar Nível 3 *",
        null=False,
        blank=False,
        related_name='nivel_3_por_conta_pagar')
    nivel_4 = models.ForeignKey(
        'CustomPlano_Conta',  
        on_delete=models.CASCADE,
        verbose_name="Pagar Nível 4 *",
        null=False,
        blank=False,
        related_name='nivel_4_por_conta_pagar')    
    n_condominio = models.ForeignKey(
        'CustomCondominio',  # Foreign key to CustomCondominio
        on_delete=models.CASCADE,
        verbose_name="Número Condominio *",
        null=False,
        blank=False)
    
    class Meta:
        db_table = 'conta_pagar'
        managed = True
        ordering = ['data_conta_pagar', 'tipo_documento_conta_pagar', 'nivel_1', 'nivel_2', 'nivel_3', 'nivel_4'] 
        unique_together = ('data_conta_pagar', 'n_documento_conta_pagar')  

    def __str__(self):
        return f"{self.data_conta_pagar} - {self.n_documento_conta_pagar} - {self.tipo_documento_conta_pagar} - {self.dsc_conta_pagar}"

