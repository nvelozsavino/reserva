"""
WSGI config for calendar_reserva project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
os.environ['HTTPS'] = "on"


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


import monitor
monitor.start(interval=1.0)