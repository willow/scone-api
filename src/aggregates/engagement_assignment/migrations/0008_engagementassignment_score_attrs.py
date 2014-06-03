# encoding: utf8
from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_assignment', '0007_recommendation'),
    ]

    operations = [
        migrations.AddField(
            model_name='engagementassignment',
            name='score_attrs',
            field=jsonfield.fields.JSONField(default=None),
            preserve_default=False,
        ),
    ]
