from django import template

register = template.Library()

@register.filter
def currency_brl(value):
    return f' {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
