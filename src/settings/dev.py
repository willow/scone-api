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

GRAPH_DB_URL = 'http://localhost:7474/db/data/'
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
  'encoding': 'UTF-8',
  }

LOGGING['handlers']['request_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/django_request.log',
  'maxBytes': 1024 * 1024 * 5, # 5 MB
  'backupCount': 5,
  'formatter': 'standard',
  'encoding': 'UTF-8',
  }

LOGGING['handlers']['exception_handler'] = {
  'level': 'ERROR',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/error.log',
  'maxBytes': 1024 * 1024 * 5, # 5 MB
  'backupCount': 5,
  'formatter': 'standard',
  'encoding': 'UTF-8',
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

########### EMAIL CONFIGURATION
SENDGRID_USERNAME = "Test_User"
SENDGRID_PASSWORD = "Password"
########## END EMAIL CONFIGURATION

########### SOCIAL PROVIDER CONFIGURATION
REDDIT_SUBREDDIT_QUERY_LIMIT = 2
########## END SOCIAL PROVIDER CONFIGURATION

#Get a developer's local overrides (if they exist)
try:
  from .dev_override import *
except:
  pass
