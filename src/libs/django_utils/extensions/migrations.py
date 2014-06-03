# http://stackoverflow.com/questions/5472925/django-loading-data-from-fixture-after-backward-migration-loaddata-is
# -using-mo/5906258#5906258

from unittest import mock


def load_data(models, fixture_name):

  def new_get_model(model_identifier):
    return models[model_identifier]

  # with mock.patch('django.core.serializers.python._get_model', new_get_model):
  from django.core.management import call_command

  call_command("loaddata", fixture_name)


def load_data_partial(fixture_name):
  def load_data_func(models, schema_editor):
    load_data(models, fixture_name)

  return load_data_func
