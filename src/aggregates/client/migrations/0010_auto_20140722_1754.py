# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_auto_20140626_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='client_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'tech startup (sass)'), (2, 'tech startup (marketing)'), (3, 'young adult author'), (4, 'tech startup (video convo)'), (5, 'tech startup (professional social networking)'), (6, 'tech startup(appointment finding affiliate)'), (7, 'tech startup(appointment finding client)'), (8, 'tech startup (sports meetup)'), (9, 'ya writing meetup')]),
        ),
    ]
