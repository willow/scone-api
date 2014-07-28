# encoding: utf8
from django.db import models, migrations
import datetime
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_profile_prospect'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='system_created_date',
            field=models.DateTimeField(default=timezone.now()),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='provider_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Twitter'), (2, 'Reddit'), (3, 'LinkedIn')]),
        ),
    ]
