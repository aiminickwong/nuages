import os
import sys


path = '/usr/share/nuages'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'nuages.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
