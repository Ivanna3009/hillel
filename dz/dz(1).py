import sys
import os.path

from random import choice

from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse,HttpResponseNotFound
from django.urls import path
import random
from importlib import import_module
from django.shortcuts import render

settings.configure(
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)),
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY='secret'
)
#mod = import_module('random')
#obj = getattr(mod, obj_name)
#text = '\t'.join(dir(mod))
template = """
<!DOCTYPE html>
<html>
<head>
 <title>{title}</title>
</head>
<body>
 <div>{doc}</div>
</body>
</html>
"""

def mod_index(request, mod_name):
    try:
        mod = import_module(mod_name)
        links=(f'<a href="{mod_name}/{name}">{name}</a>'
                for name in dir(mod) if not name[0]=='_')
        return HttpResponse(template.format(title=f'Index of {mod_name}',
                                            doc='<br>'.join(links)))
    except Exception as e:
        return HttpResponseNotFound(e)

def doc(request, mod_name, name):
    try:
        mod = import_module(mod_name)
        return HttpResponse(getattr(mod, name).__doc__,
                            content_type='text/plain')
    except Exception as e:
        return HttpResponseNotFound(e)
urlpatterns = [
    path('doc/<mod_name>', mod_index),
    path('doc/<mod_name>/<name>', doc)
]

if __name__ == '__main__':
    execute_from_command_line()
