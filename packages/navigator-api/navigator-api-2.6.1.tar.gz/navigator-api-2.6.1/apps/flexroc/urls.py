"""Urls.

List of program routes.
"""
from navigator.routes import path # always required
from apps.flexroc.views import other, handler

urls = [
    path('get', '/hola', handler, name='hola_flexroc'),
    path('get', '/other', other, name='hola_mundo'),
]
