# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_auto_20140522_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'tech startup (sass)'), (2, 'tech startup (marketing)'), (3, 'young adult author')]),
        ),
    ]
