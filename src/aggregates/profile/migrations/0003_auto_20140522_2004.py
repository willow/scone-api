# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_neo_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='provider_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Twitter'), (2, 'Reddit')]),
        ),
    ]
