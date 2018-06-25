from django import template

register = template.Library()

@register.filter(name='add')
def add(value):
    return value+1
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

