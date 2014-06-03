"""Production settings and globals."""


import dj_database_url
import os

import sys
import urllib.parse

from .common import *


########## EMAIL CONFIGURATION
# See: Django Skel for more examples
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {'default': dj_database_url.config()}

# See: https://docs.djangoproject.com/en/dev/ref/databases/#persistent-database-connections
CONN_MAX_AGE = 60

GRAPH_DB_URL = environ['GRAPH_DB_URL']
GRAPH_DB_USERNAME = environ['GRAPH_DB_USERNAME']
GRAPH_DB_PASSWORD = environ['GRAPH_DB_PASSWORD']
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
redis_url = urllib.parse.urlparse(os.environ.get('REDISCLOUD_URL'))
CACHES = {
  'default': {
    'BACKEND': 'redis_cache.RedisCache',
    'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
    'OPTIONS': {
      'PASSWORD': redis_url.password,
      'DB': 0,
      }
  }
}
########## END CACHE CONFIGURATION


########## LOGGING CONFIGURATION
# See: Raven sends errors to sentry
INSTALLED_APPS += (
  'raven.contrib.django.raven_compat',
)

APP_LOG_LEVEL = os.environ.get('APP_LOG_LEVEL', 'INFO')

LOGGING['handlers']['console_handler'] = {
  'level': APP_LOG_LEVEL,
  'class': 'logging.StreamHandler',
  'formatter': 'standard',
  'stream': sys.stdout # http://stackoverflow.com/questions/11866322/heroku-logs-for-django-projects-missing-errors
}

LOGGING['handlers']['exception_handler'] = {
  'level': 'ERROR',
  'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
  }

app_logger = {
  'handlers': ['console_handler', 'exception_handler'],
  'level': APP_LOG_LEVEL,
  'propagate': False
}

LOGGING['loggers'] = {
  '': {
    'handlers': ['console_handler'],
    'level': APP_LOG_LEVEL,
    'propagate': True
  },
  'django.request': {
    'handlers': ['console_handler'],
    'level': 'WARNING',
    'propagate': False
  },
  'django.db.backends': {
    'level': APP_LOG_LEVEL,
  },
  'src.aggregates': app_logger,
  'src.apps': app_logger,
  'celery': app_logger,
  'src.libs': app_logger
}
########## END LOGGING CONFIGURATION

########## CELERY CONFIGURATION
# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
# https://devcenter.heroku.com/articles/rabbitmq-bigwig#provisioning-the-add-on
celery_rabbit_url = os.environ['RABBITMQ_BIGWIG_RX_URL']
BROKER_URL = celery_rabbit_url

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
########## END CELERY CONFIGURATION

########## STORAGE CONFIGURATION
# See: Django skell for robust examples
########## END STORAGE CONFIGURATION


########## COMPRESSION CONFIGURATION
# See: Django skell for robust examples
########## END COMPRESSION CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = environ['SECRET_KEY']
########## END SECRET CONFIGURATION

########## ALLOWED HOSTS CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.herokuapp.com', 'qa.api.wifl.com']
########## END ALLOWED HOST CONFIGURATION

########## CORS CONFIGURATION
CORS_ORIGIN_REGEX_WHITELIST = (
  '^http(s)?://qa.wifl\.com/?',
  '^http://localhost:\d{1,4}/?',
)
########## END CORS CONFIGURATION

########### SOCIAL PROVIDER CONFIGURATION
TWITTER_APP_KEY = environ['TWITTER_APP_KEY']
TWITTER_APP_SECRET = environ['TWITTER_APP_SECRET']
########## END SOCIAL PROVIDER CONFIGURATION

########### NLP CONFIGURATION
ALCHEMY_API_KEY = environ['ALCHEMY_API_KEY']
########## END NLP CONFIGURATION

########### DRIVE CONFIGURATION
DRIVE_USERNAME = environ['DRIVE_USERNAME']
DRIVE_PASSWORD = environ['DRIVE_PASSWORD']
DRIVE_ASSIGNMENT_SPREADSHEET_KEY = environ['DRIVE_ASSIGNMENT_SPREADSHEET_KEY']
########## END DRIVE CONFIGURATION

# ########## API CONFIGURATION
EXTERNAL_API_TOKEN = environ['EXTERNAL_API_TOKEN']
########## END API CONFIGURATION

########### EMAIL CONFIGURATION
SENDGRID_USERNAME = environ['SENDGRID_USERNAME']
SENDGRID_PASSWORD = environ['SENDGRID_PASSWORD']
########## END EMAIL CONFIGURATION
