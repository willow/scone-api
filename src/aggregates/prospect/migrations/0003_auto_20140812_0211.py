# encoding: utf8
from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('prospect', '0002_neo_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prospect',
            name='prospect_attrs',
            field=jsonfield.fields.JSONField(),
        ),
    ]
