from django.core import management
from django.conf import settings
import pytest
from src.libs.graphdb_utils.services import graphdb_provider

"""
The _db_with_migrations_marker is a pattern used by pytest-django.
Pytest itself doesn't look for that naming conventions. The convention is to use Autouser=True and then look for a
fixture. This is a convenient mechanism so you don't actually need to rely on a fixture.
"""

@pytest.fixture(scope='session')
def enable_south_migrations():
  # this was taken directly from the pycharm test runner
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


@pytest.fixture(scope='session')
def _graph_db_setup(request):
  graph_db = graphdb_provider.get_graph_client()

  def clean_db():
    graph_db.query("""MATCH (n)
    OPTIONAL MATCH (n)-[r]-()
    DELETE n,r""")

  clean_db()

  def fin():
    clean_db()
    graph_db.flush()

  request.addfinalizer(fin)

@pytest.fixture(autouse=True, scope='function')
def _graph_db_marker(request):
  marker = request.keywords.get('graph_db', None)
  if marker:
    request.getfuncargvalue('graph_db')

@pytest.fixture(scope='function')
def graph_db(request, _graph_db_setup):
  graph_db = graphdb_provider.get_graph_client()
  # it is important to have `update` be True. This allows the content from the requests to update the QuerySequences
  # immediately and won't re-run the query and re-hit neo4j. This is important because during a test, if you try to
  # re-hit neo4j it'll return a 404 error. This took a while to figure out when I set update=False.
  tx = graph_db.transaction(using_globals=True, commit=False, for_query=True)

  def fin():
    tx.rollback()
    graph_db.flush()

  request.addfinalizer(fin)

  return graph_db
