# -*- coding> utf-8 -*-
import os
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import escape
from django import template
from .forms import PostForm
register = template.Library()

@register.filter
def ssplit(str, word):
    return word.split('.')[0]

def index(request):
    p = re.compile(r"[silvio|screen|minino]")
    diretorios = filter(None, [ x for x in os.listdir("/usr/local/www/kanazuchi/blog/static/fotas_site") if os.path.isdir('/usr/local/www/kanazuchi/blog/static/fotas_site/{}'.format(x)) if 'thumb' not in x if 'ultima' not in x if 'mid' not in x ])
    uri = request.META["REQUEST_URI"]
    ultimas = [ d for d in os.listdir('/usr/local/www/kanazuchi/blog/static/fotas_site/thumb_ultimas/') if not p.match(d) ]
    n_dirs = {}
    for x in diretorios:
        n_dirs[x] = sorted(set(os.listdir("/usr/local/www/kanazuchi/blog/static/fotas_site/{}".format(x))))[0]
    return render(request, 'blog/index.html', {'uri': uri, 'diretorios': diretorios, 'n_dirs': n_dirs, 'ultimas': ultimas})

def galery(request):
    diretorio = request.GET.get('dir')
    images = os.listdir('/usr/local/www/kanazuchi/blog/static/fotas_site/{}/'.format(diretorio))
    return render(request, 'blog/galery.html', {'images': images, 'diretorio': diretorio})

def spdsw(request):
    d = {}
    if request.method == "POST":
        for i in request.META:
            if 'wsgi' not in i and i != 'DOCUMENT_ROOT':
                d[i] = request.META.get(i)
        form = PostForm(request.POST)
        post = form.save(commit=False)
        post.save()
        return render(request, 'blog/spdsw.html', {'d': d, 'form': form, 'pk': post.pk})
    else:
        form = PostForm()
        return render(request, 'blog/spdsw.html', {'d': d, 'form': form})

def teste(request):
    d = {}
    for i in request.META:
        if 'wsgi' not in i and i != 'DOCUMENT_ROOT':
            d[i] = request.META.get(i)
    return render(request, 'blog/teste.html', {'d': d})

def about(request):
    return render(request, 'blog/about.html', {})

def fogonorabo(request):
    return render(request, 'blog/fogonorabo.html', {})

def tarik(request):
    return render(request, 'blog/tarik.html', {})

def familia(request):

    read_json = filter(None, open('/usr/local/www/kanazuchi/static/familia.json', 'r').read().split("\n"))
    list_json = []
    for x in read_json:
        _x = x.split(',')
        for i in _x[1:-1]:
            list_json.append({"source": i.rstrip(), "target": _x[0], "group": _x[-1]})
    len_list_json = len(list_json)

    return render(request, 'blog/familia.html', {'list_json': list_json, 'len_list_json': len_list_json})
