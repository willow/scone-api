# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_opportunity', '0004_auto_20140502_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='engagementopportunity',
            name='provider_action_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Twitter'), (2, 'Reddit')], default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='engagementopportunity',
            name='system_created_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='engagementopportunity',
            name='created_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='engagementopportunity',
            name='provider_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Twitter'), (2, 'Reddit')]),
        ),
    ]
