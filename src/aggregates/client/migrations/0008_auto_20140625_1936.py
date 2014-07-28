# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_auto_20140621_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'tech startup (sass)'), (2, 'tech startup (marketing)'), (3, 'young adult author'), (4, 'tech startup (video convo)'), (5, 'tech startup (professional social networking)'), (6, 'tech startup(appointment finding affiliate)')]),
        ),
    ]
