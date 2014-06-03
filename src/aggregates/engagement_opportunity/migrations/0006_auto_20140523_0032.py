# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_opportunity', '0005_auto_20140522_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engagementopportunity',
            name='provider_action_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Tweet'), (2, 'Reddit Comment'), (3, 'Reddit Self Post'), (4, 'Reddit Link Post')]),
        ),
    ]
