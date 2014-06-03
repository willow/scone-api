import os

from celery import Celery
from django.conf import settings

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings.dev')

app = Celery('app')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# For Celery Beat to use Django for periodic tasks, we need to make sure the Periodic Task models are ready to go.
django.setup()

# Celery logging must be Greater Than DEBUG:
# There is a bug in djcelery/schedulers.py on line 253:
#   repr(entry) for entry in self._schedule.itervalues()),
# So, for python3, itervalues will raise an error.
