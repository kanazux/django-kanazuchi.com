from django import template


register = template.Library()


@register.filter(name='replace_')
def replace_(str, word):
    return word.replace('_', ' ')
