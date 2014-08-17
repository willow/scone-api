# encoding: utf8
from django.db import models, migrations
import jsonfield.fields


def update_func(models, schema_editor):
  Prospect = models.get_model("prospect", "Prospect")
  Prospect.objects.filter(prospect_attrs=None).update(prospect_attrs={})


class Migration(migrations.Migration):
  dependencies = [
    ('prospect', '0002_neo_index'),
  ]

  operations = [
    migrations.RunPython(update_func),
    migrations.AlterField(
      model_name='prospect',
      name='prospect_attrs',
      field=jsonfield.fields.JSONField(),
    ),
  ]
