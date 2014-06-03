"""Common settings and globals."""

from datetime import timedelta
from os import environ
from os.path import abspath, basename, dirname, join, normpath
from sys import path
from kombu.serialization import register
from src.libs.django_utils.serialization.json_serializer_registration import json_flex_dumps, json_flex_loads
# http://stackoverflow.com/questions/21631878/celery-is-there-a-way-to-write-custom-json-encoder-decoder

# ######### PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:

DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
SYSTEM_EMAIL = ('System', 'system@wifl.com')
PUBLIC_EMAIL = ('wifl', 'info@wifl.com')
ADMIN_EMAIL = ('Admin', 'admin@wifl.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
  ADMIN_EMAIL,
)
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-DATABASE-ATOMIC_REQUESTS
ATOMIC_REQUESTS = True
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(DJANGO_ROOT, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = []

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = r"to(rkb!6lj3bwbz&qs2go0@)1ctjcx43lm6lerci#s_vpg*%mr"
########## END SECRET CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
  normpath(join(DJANGO_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
  'django.core.context_processors.static',
  'django.core.context_processors.tz',
  'django.contrib.messages.context_processors.messages',
  'django.core.context_processors.request',
)


# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
  normpath(join(DJANGO_ROOT, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
  # Use GZip compression to reduce bandwidth.
  'django.middleware.gzip.GZipMiddleware',

  # Default Django middleware.
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  # Enabled in 1.6
  # See: https://docs.djangoproject.com/en/dev/ref/clickjacking/#clickjacking-prevention
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'corsheaders.middleware.CorsMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
  # Default Django apps:
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',

  # Useful template tags:
  'django.contrib.humanize',

  # Admin panel and documentation:
  'django.contrib.admin',
  'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
  # Static file management:

  # Asynchronous task queue:
  'djcelery',
  'kombu.transport.django',

  # Database
  'reversion',
  'django_hstore',

  # Analytics

  # Rest API
  'rest_framework',

  #Headers
  'corsheaders',
)

LOCAL_APPS = (
  # AGGREGATES
  'src.aggregates.client',
  'src.aggregates.engagement_assignment',
  'src.aggregates.engagement_opportunity',
  'src.aggregates.profile',
  'src.aggregates.topic',

  # APPS
  'src.apps.engagement_discovery',
  'src.apps.graph',

  # LIBS
  'src.libs.common_domain',
  'src.libs.communication_utils',
  'src.libs.django_utils',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION


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

#there is a bug with celery 3.0 where the logger doesn't display the task id, unique id, worker, name etc
#https://github.com/celery/django-celery/issues/211

#why celery logs all as warning: http://stackoverflow.com/questions/12664250/celery-marks-all-output-as-warning

LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': {
    'standard': {
      'format': '[%(levelname)s] %(name)s: %(message)s'
    },
  },
  'handlers': {}
}
########## END LOGGING CONFIGURATION


########## CELERY CONFIGURATION
CELERY_LONGEST_RUNNING_TASK_SECONDS = 60 * 60 * 2  #seconds * minutes * hours = 2 hours
# See: http://celery.readthedocs.org/en/latest/configuration.html#celery-task-result-expires
CELERY_TASK_RESULT_EXPIRES = timedelta(seconds=CELERY_LONGEST_RUNNING_TASK_SECONDS)

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-accept-content
# 3.2 is going to remove pickle http://docs.celeryproject.org/en/latest/whatsnew-3.1.html#last-version-to-enable
# -pickle-by-default

register('json', json_flex_dumps, json_flex_loads,
         content_type='application/json',
         content_encoding='utf-8')

CELERY_TASK_SERIALIZER = 'json'

CELERY_IMPORTS = (
  'src.apps.engagement_discovery.services.engagement_discovery_tasks',
  'src.apps.assignment_delivery.services.assignment_delivery_tasks',
  'src.aggregates.client.services.client_tasks',
  'src.libs.communication_utils.services.email_tasks',
)

# See: http://docs.celeryproject.org/en/master/configuration.html#celery-acks-late
CELERY_ACKS_LATE = True
########## END CELERY CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
########## END WSGI CONFIGURATION


########## COMPRESSION CONFIGURATION
# See django skel for more info
########## END COMPRESSION CONFIGURATION


########### EMAIL CONFIGURATION
SPAM_SCORE_THRESHOLD = environ.get('SPAM_SCORE_THRESHOLD', 2.3)
########## END EMAIL CONFIGURATION


########### REST CONFIGURATION
REST_FRAMEWORK = {
  # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
  'PAGINATE_BY': 10
}
########## END REST CONFIGURATION


########## CORS CONFIGURATION
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_CREDENTIALS = True
########## END CORS CONFIGURATION


########### SOCIAL PROVIDER CONFIGURATION
REDDIT_USER_AGENT = 'WiFL v0.1 https://github.com/WiFL-co'
REDDIT_SUBREDDIT_QUERY_LIMIT = 10
########## END SOCIAL PROVIDER CONFIGURATION
