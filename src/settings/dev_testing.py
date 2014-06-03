"""Development settings and globals."""


from .dev import *

########## CELERY CONFIGURATION
# Integration tests require the tasks to be excuted eagerly. If celery doesn't run this way, the events won't occur
# and the tests will fail.
# See: http://docs.celeryq.org/en/latest/configuration.html#celery-always-eager
CELERY_ALWAYS_EAGER = True

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
BROKER_URL = 'django://'

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
########## END CELERY CONFIGURATION
