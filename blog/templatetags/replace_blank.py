from django import template


register = template.Library()


@register.filter(name='replace_blank')
def replace_blank(str, word):
    if word == "":
        return bytes("Empty", encoding='utf-8')
    else:
        return word
