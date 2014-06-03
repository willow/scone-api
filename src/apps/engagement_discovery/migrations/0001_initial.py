from django.db import migrations

from src.libs.django_utils.extensions.migrations import load_data_partial


class Migration(migrations.Migration):
  dependencies = [
  ]

  operations = [
    migrations.RunPython(load_data_partial("0001_initial.json")),
  ]
