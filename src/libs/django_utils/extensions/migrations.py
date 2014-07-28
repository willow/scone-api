# http://stackoverflow.com/questions/5472925/django-loading-data-from-fixture-after-backward-migration-loaddata-is
# -using-mo/5906258#5906258


def load_data(models, fixture_name):
  from django.core.management import call_command

  call_command("loaddata", fixture_name)


def load_data_partial(fixture_name):
  def load_data_func(models, schema_editor):
    load_data(models, fixture_name)

  return load_data_func
