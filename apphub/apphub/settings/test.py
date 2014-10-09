from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'apphub',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': '10.10.93.39',
        'PORT': 3306,
    }
}
