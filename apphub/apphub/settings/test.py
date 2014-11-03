from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'apphub',
        'USER': 'solar',
        'PASSWORD': '!@#solar',
        'HOST': '10.13.85.89',
        'PORT': 3306,
    }
}


REST_FRAMEWORK.update({
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',)
})

DATA_SYNC_API = "http://t2.ams.sohuno.com/api/sync_from_spider"
