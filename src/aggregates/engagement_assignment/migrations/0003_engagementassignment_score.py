# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_assignment', '0002_neo_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='engagementassignment',
            name='score',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
