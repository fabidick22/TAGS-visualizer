from django import template

register = template.Library()

@register.filter(name='get_value_key')
def return_value(value, arg):
    return value[arg]

@register.filter(name='convert_por')
def conver_porcentaj(value, arg):
    return (100*value)/arg

@register.filter(name='contarKeys')
def conver_porcentaj(value, arg):
    return len(value.keys())