# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0002_neo_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='topic_type',
        ),
    ]
