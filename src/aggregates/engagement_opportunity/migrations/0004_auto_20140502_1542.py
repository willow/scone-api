# encoding: utf8
from django.db import models, migrations
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_opportunity', '0003_engagementopportunitytopic'),
    ]

    operations = [
        migrations.AddField(
            model_name='engagementopportunity',
            name='system_created_date',
            field=models.DateTimeField(default=timezone.now()),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='engagementopportunity',
            name='created_date',
            field=models.DateTimeField(default=timezone.now()),
            preserve_default=True,
        ),
    ]
