# -*- coding: utf-8 -*-


import os
import re
from .forms import IpyForm
from .forms import PostForm
from django import template
from django.shortcuts import render
from random import randint, shuffle
from ipy_show import return_ip_data


register = template.Library()


@register.filter
def ssplit(str, word):
    return word.split('.')[0]


@register.filter
def replace_(word):
    return word.replace('_', ' ')


def index(request):
    p = re.compile(r"[silvio|screen|minino]")
    diretorios = filter(None, [x for x in os.listdir(
        "/usr/local/www/kanazuchi/blog/static/fotas_site") if os.path.isdir(
            '/usr/local/www/kanazuchi/blog/static/fotas_site/{}'.format(x))
                               if 'thumb' not in x if 'ultima' not in x
                               if 'mid' not in x])
    # uri = request.META["REQUEST_URI"]
    ultimas = [d for d in os.listdir(
        '/usr/local/www/kanazuchi/blog/static/fotas_site/thumb_ultimas/')
               if not p.match(d)]
    n_dirs = {}
    for x in diretorios:
        n_dirs[x] = sorted(
            set(os.listdir(
                "/usr/local/www/kanazuchi/blog/static/fotas_site/{}".format(
                    x))))[0]
    return render(request, 'blog/index.html', {'diretorios': diretorios,
                                               'n_dirs': n_dirs,
                                               'ultimas': ultimas})


def galery(request):
    diretorio = request.GET.get('dir')
    images = os.listdir(
        '/usr/local/www/kanazuchi/blog/static/fotas_site/{}/'.format(
            diretorio))
    return render(request, 'blog/galery.html', {'images': images,
                                                'diretorio': diretorio})


def ipytest(request):

    def get_ip():
        field_1 = ['10', '172', '192']
        shuffle(field_1)
        if field_1[0] == '10':
            field_2 = randint(0, 255)
            field_net = randint(8, 24)
        elif field_1[0] == '172':
            field_2 = randint(16, 31)
            field_net = randint(8, 24)
        elif field_1[0] == '192':
            field_2 = '168'
            field_net = randint(8, 24)
        field_3 = randint(0, 255)
        field_4 = randint(1, 254)
        return "{}.{}.{}.{}".format(
            field_1[0], field_2, field_3, field_4), str(field_net)

    form = IpyForm()
    # url_pattern = re.compile(r"([0-9]{1,3}\.){3}[0-9]{1,3}\/[1-3]?[0-9]")
    print_output = None
    print_help = None
    output = ""
    phelp = ["The fields must be filled with correctly values.",
             "Example for IP 192.168.0.1/24:",
             "Binary Ip: 11000000.10101000.00000000.00000001",
             "Binary Mask: 11111111.11111111.11111111.00000000",
             "CIDR Mask: 255.255.255.0",
             "Broadcast IP: 192.168.0.255",
             "Network IP: 192.168.0.1"]
    ip_mask = "/".join(get_ip())
    if request.method == "POST":
        new_form = request.POST
        ip_mask = new_form['ip_mask']
        ip, mask = ip_mask.split('/')
        ip_data = return_ip_data(ip, mask)
        error_fields = []
        if new_form['binary_ip'] != ip_data['Binary_Ip']:
            error_fields.append(("Wrong Binary Ip", new_form['binary_ip']))
        if new_form['binary_mask'] != ip_data['Binary_Mask']:
            error_fields.append(("Wrong Binary Mask", new_form['binary_mask']))
        if new_form['broadcast_ip'] != ip_data['Broadcast_Ip']:
            error_fields.append(("Wrong Broadcast", new_form['broadcast_ip']))
        if new_form['cidr_mask'] != ip_data['Full_Mask']:
            error_fields.append(("Wrong CIDR Mask", new_form['cidr_mask']))
        if new_form['network_ip'] != ip_data['Network_Ip']:
            error_fields.append(("Wrong Network Ip", new_form['network_ip']))
        if " {} ".format(new_form['class_ip']) not in ip_data['Class']:
            error_fields.append(("Wrong Class Ip", new_form['class_ip']))
        if len(error_fields) == 0:
            output = [(x, ip_data[x]) for x in ip_data]
            print_output = True
            form = False
        else:
            print_help = True
        return render(
            request, 'blog/ipytest.html', {'form': form,
                                           'error_fields': error_fields,
                                           'output': output,
                                           'print_help': print_help,
                                           'print_output': print_output,
                                           'phelp': phelp,
                                           'ip_mask': ip_mask})
    return render(request, 'blog/ipytest.html', {'form': form,
                                                 'output': output,
                                                 'print_help': print_help,
                                                 'print_output': print_output,
                                                 'ip_mask': ip_mask,
                                                 'phelp': phelp})


def ipyshow(request):

    form = PostForm()
    url_pattern = re.compile(r"([0-9]{1,3}\.){3}[0-9]{1,3}\/[1-3]?[0-9]")
    print_output = None
    print_help = None
    output = ""
    phelp = ["The ipy-show gets an ip and mask in slash notation.",
             "IP can not be 0.0.0.0 and mask must be in range 1, 32.",
             " Usage: ipy-show <ip/mask>",
             " Example: ipy-show 10.47.31.5/11"]
    if request.method == "POST":
        if bool(url_pattern.match(request.POST['ip'])):
            ip, mask = request.POST['ip'].split('/')
            if int(mask) in list(range(1, 33)):
                get_data = return_ip_data(ip, mask)
                output = [(x, get_data[x]) for x in get_data]
                print_output = True
            else:
                print_help = True
        else:
            print_help = True
    return render(request, 'blog/ipyshow.html', {'form': form,
                                                 'output': output,
                                                 'print_help': print_help,
                                                 'print_output': print_output,
                                                 'phelp': phelp})


def teste(request):
    d = {}
    for i in request.META:
        if 'wsgi' not in i and i != 'DOCUMENT_ROOT':
            d[i] = request.META.get(i)
    return render(request, 'blog/teste.html', {'d': d})


def about(request):
    return render(request, 'blog/about.html', {})


def familia(request):
    read_json = filter(None, open(
        '/usr/local/www/kanazuchi/static/familia.json',
        'r').read().split("\n"))
    list_json = []
    for x in read_json:
        _x = x.split(',')
        for i in _x[1:-1]:
            list_json.append(
                {"source": i.rstrip(), "target": _x[0], "group": _x[-1]})
    len_list_json = len(list_json)

    return render(request, 'blog/familia.html',
                  {'list_json': list_json, 'len_list_json': len_list_json})
