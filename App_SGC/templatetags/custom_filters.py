from django import template
register = template.Library()
import datetime



# Formata o CPF
@register.filter(name='format_cpf')
def format_cpf(value):
    # Remove qualquer caractere não numérico
    cpf = ''.join(filter(str.isdigit, value))
    
    # Aplica a máscara de CPF de acordo com o número de dígitos
    if len(cpf) == 11:
        return '{}.{}.{}-{}'.format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
    elif len(cpf) == 10:
        return '{}.{}.{}-{}'.format(cpf[:2], cpf[2:5], cpf[5:8], cpf[8:])
    
    # Retorna o valor original se o CPF não tiver 10 ou 11 dígitos
    return value


# Formata números decimais
@register.filter
def currency_brl(value):
    try:
        if value is None:
            return ''  # Return an empty string for None
        return f'{float(value):,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return ''  # Return an empty string for invalid input
    

# Formata o número do celular
@register.filter(name='format_celular')
def format_celular(value):
    """
    Formata o número de celular no formato (xx) xxxxx-xxxx
    """
    if value and len(value) == 11:
        return f"({value[:2]}) {value[2:7]}-{value[7:]}"
    return value


#  Formata a data xx/xx/xx
@register.filter(name='format_date')
def format_date(value):
    """
    Formata uma data no formato dd/mm/aa.
    """
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.strftime('%d/%m/%y')
    return value  # Retorna o valor original se não for uma data

# Formata uma data no formato MM/YYYY.
@register.filter(name='format_month_year')
def format_date(value):
    """
    Aceita strings no formato 'YYYY-MM' ou objetos de data (datetime.date).
    """
    if isinstance(value, str) and len(value) == 7 and '-' in value:
        # Se a string estiver no formato 'YYYY-MM'
        ano, mes = value.split('-')
        return f"{mes}/{ano}"
    elif isinstance(value, (datetime.date, datetime.datetime)):
        # Se for um objeto de data, formata no estilo MM/YYYY
        return value.strftime('%m/%Y')
    return value  # Retorna o valor original se não for uma data válida

# Formata o horário em 24 h. (xx:xx)
@register.filter(name='format_time')
def format_time(value):
    """
    Formata um horário no formato 24 horas (xx:xx).
    """
    if isinstance(value, (datetime.time, datetime.datetime)):
        return value.strftime('%H:%M')
    return value  



# trunca o link do arquivo para 20 caracteres
@register.filter(name='truncate_document')
def truncate_document(value, length=20):
    """
    Trunca o nome do arquivo para o número de caracteres especificado (20 por padrão),
    adicionando '...' no final.
    """
    if hasattr(value, 'name'):
        value = value.name  # Acessa o nome do arquivo se for um FieldFile
    if len(value) > length:
        return value[:length] + '...'
    return value



# Multiplica dois valores que são passados
@register.filter
def multiply(value, arg):
    return value * arg
