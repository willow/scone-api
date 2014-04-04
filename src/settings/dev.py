"""Development settings and globals."""


from os.path import join, normpath

from .common import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(DJANGO_ROOT, 'default.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
  }
}

########## END CACHE CONFIGURATION

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
#celery hijacks its logging to prevent other libs from screwing it up. In dev only, it'd be nice to write to a log file.
#http://docs.celeryproject.org/en/latest/configuration.html#logging
#why: http://stackoverflow.com/a/6942030/173957
#code: /celery/app/log.py
#if self.app.conf.CELERYD_HIJACK_ROOT_LOGGER:
#  root.handlers = []

# celery controls the root logging behavior with --loglevel=LEVEL
# we've set it to DEBUG so that our app controls the levels.

CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_REDIRECT_STDOUTS = False

LOGGING['handlers']['console_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.StreamHandler',
  'formatter': 'standard'
}

LOGGING['handlers']['file_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/app.log',
  'maxBytes': 1024 * 1024 * 5, # 5 MB
  'backupCount': 5,
  'formatter': 'standard',
  }

LOGGING['handlers']['request_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/django_request.log',
  'maxBytes': 1024 * 1024 * 5, # 5 MB
  'backupCount': 5,
  'formatter': 'standard',
  }

LOGGING['handlers']['exception_handler'] = {
  'level': 'ERROR',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/error.log',
  'maxBytes': 1024 * 1024 * 5, # 5 MB
  'backupCount': 5,
  'formatter': 'standard',
  }

app_logger = {
  'handlers': ['console_handler', 'file_handler', 'exception_handler'],
  'level': 'DEBUG',
  'propagate': False
}

LOGGING['loggers'] = {
  '': {
    'handlers': ['console_handler', 'file_handler'],
    'level': 'DEBUG',
    'propagate': True
  },
  'django.request': {
    'handlers': ['request_handler', 'exception_handler', 'console_handler'],
    'level': 'DEBUG',
    'propagate': False
  },
  'celery': {
    'level': 'INFO',
  },
  'django.db.backends': {
    'level': 'INFO',
  },
  'src.aggregates': app_logger,
  'src.apps': app_logger,
  'src.libs': app_logger,
  'celery.task': app_logger
  #there is a bug with celery 3.0 where the logger doesn't display the task id, unique id, worker, name etc
  #https://github.com/celery/django-celery/issues/211

  #why celery logs all as warning: http://stackoverflow.com/questions/12664250/celery-marks-all-output-as-warning
}
########## END LOGGING CONFIGURATION

########## CELERY CONFIGURATION
# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
BROKER_URL = 'django://'

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
########## END CELERY CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
)
########## END TOOLBAR CONFIGURATION


########## TESTING CONFIGURATION
########## END TESTING CONFIGURATION


########## CORS CONFIGURATION
CORS_ORIGIN_REGEX_WHITELIST = (
  '^http://localhost:\d{1,4}/?',
)
########## END CORS CONFIGURATION

########## DJANGO EXTENSIONS CONFIGURATION
INSTALLED_APPS += (
  'django_extensions',
)
########## END DJANGO EXTENSIONS CONFIGURATION

#Get a developer's local overrides (if they exist)
try:
  from dev_override import *
except:
  pass
