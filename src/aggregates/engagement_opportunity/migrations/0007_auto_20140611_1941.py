# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_opportunity', '0006_auto_20140523_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engagementopportunity',
            name='provider_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Twitter'), (2, 'Reddit'), (3, 'LinkedIn')]),
        ),
    ]
