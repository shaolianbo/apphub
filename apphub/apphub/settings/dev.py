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
