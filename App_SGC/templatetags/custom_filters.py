from django import template

register = template.Library()

@register.filter
def currency_brl(value):
    try:
        if value is None:
            return ''  # Return an empty string for None
        return f'{float(value):,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return ''  # Return an empty string for invalid input
    

