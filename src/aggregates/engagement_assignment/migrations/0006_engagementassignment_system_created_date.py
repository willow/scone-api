# encoding: utf8
from django.db import models, migrations
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_assignment', '0005_auto_20140501_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='engagementassignment',
            name='system_created_date',
            field=models.DateTimeField(default=timezone.now()),
            preserve_default=False,
        ),
    ]
