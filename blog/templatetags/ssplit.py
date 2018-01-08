from django import template
register = template.Library()

@register.filter(name='ssplit')
def ssplit(str, word):
	return word.split('.')[0]
