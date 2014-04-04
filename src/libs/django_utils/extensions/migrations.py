#http://stackoverflow.com/questions/5472925/django-loading-data-from-fixture-after-backward-migration-loaddata-is-using-mo/5906258#5906258
from dingus import patch


def load_data(orm, fixture_name):
  _get_model = lambda model_identifier: orm[model_identifier]

  with patch('django.core.serializers.python._get_model', _get_model):
    from django.core.management import call_command

    call_command("loaddata", fixture_name)
