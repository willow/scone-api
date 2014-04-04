import os
import pytest

# region DJ Settings
#http://pytest-django.readthedocs.org/en/latest/configuring_django.html#using-django-configurations
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings.dev_testing")
# endregion

# region Plugins
#this line is required in order to use the db_with_migrations fixture
#http://pytest.org/latest/plugins.html#requiring-loading-plugins-in-a-test-module-or-conftest-file
pytest_plugins = "src.libs.django_utils.testing.utils"
# endregion

# region test type command line options
#configure which tests run when: http://pytest.org/latest/example/simple
# .html#control-skipping-of-tests-according-to-command-line-option
def pytest_addoption(parser):
  parser.addoption("--test-type", default='unit', help="run specific test type (unit, integration, etc.)")


def pytest_runtest_setup(item):
  test_type_specified = item.config.getoption("--test-type")
  test_type_found = os.path.basename(item.fspath.dirname).lower()
  if test_type_found != test_type_specified:
    pytest.skip("Test type: {0} was specified but test type was: {1}".format(test_type_specified, test_type_found))

# endregion
