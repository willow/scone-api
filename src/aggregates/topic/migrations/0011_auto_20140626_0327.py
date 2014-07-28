# encoding: utf8
from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0010_auto_20140625_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtopic',
            name='subtopic_attrs',
            field=jsonfield.fields.JSONField(blank=True),
        ),
    ]
