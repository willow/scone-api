from django.core import management
from django.conf import settings
import pytest


@pytest.fixture(scope='session')
def enable_south_migrations():
  #this was taken directly from the pycharm test runner
  management.get_commands()
  if hasattr(settings, "SOUTH_TESTS_MIGRATE") and not settings.SOUTH_TESTS_MIGRATE:
    # point at the core syncdb command when creating tests
    # tests should always be up to date with the most recent model structure
    management._commands['syncdb'] = 'django.core'
  elif 'south' in settings.INSTALLED_APPS:
    try:
      from south.management.commands import MigrateAndSyncCommand

      management._commands['syncdb'] = MigrateAndSyncCommand()
      from south.hacks import hacks

      if hasattr(hacks, "patch_flush_during_test_db_creation"):
        hacks.patch_flush_during_test_db_creation()
    except ImportError:
      management._commands['syncdb'] = 'django.core'


@pytest.fixture(scope='function')
def db_with_migrations(enable_south_migrations, db):
  pass


@pytest.fixture(autouse=True)
def _django_db_with_migrations_marker(request):
  marker = request.keywords.get('django_db_with_migrations', None)
  if marker:
    validate_django_db_with_migrations(marker)
    if marker.transaction:
      raise NotImplementedError('transactional_db_with_migrations needs to be created still')
    else:
      request.getfuncargvalue('db_with_migrations')


def validate_django_db_with_migrations(marker):
  def apifun(transaction=False):
    marker.transaction = transaction

  apifun(*marker.args, **marker.kwargs)
