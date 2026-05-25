"""
WSGI config para o projeto portfolio.

Expoe o callable WSGI como variavel de modulo chamada ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

application = get_wsgi_application()
