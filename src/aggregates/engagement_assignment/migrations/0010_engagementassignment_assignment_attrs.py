# encoding: utf8
from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_assignment', '0009_auto_20140606_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='engagementassignment',
            name='assignment_attrs',
            field=jsonfield.fields.JSONField(default=0),
            preserve_default=False,
        ),
    ]
