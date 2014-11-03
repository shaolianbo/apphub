from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'apphub',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}

DATA_SYNC_API = 'http://0.0.0.0:8000/api/sync_from_spider'
