# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_neo_index'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tatopic',
            unique_together=set([('client', 'topic_type')]),
        ),
    ]
