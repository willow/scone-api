# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_assignment', '0008_engagementassignment_score_attrs'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='engagementassignment',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='engagementassignment',
            name='engagement_opportunity',
        ),
    ]
