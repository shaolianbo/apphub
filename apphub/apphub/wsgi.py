"""
WSGI config for apphub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
profile = os.environ.setdefault("APPHUB_PROFILE", "dev")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apphub.settings.%s" % profile)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
