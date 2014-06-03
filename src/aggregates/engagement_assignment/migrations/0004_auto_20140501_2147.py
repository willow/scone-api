# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_assignment', '0003_engagementassignment_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engagementassignment',
            name='score',
            field=models.FloatField(db_index=True),
        ),
    ]
