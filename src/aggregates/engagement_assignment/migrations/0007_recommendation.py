# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_assignment', '0006_engagementassignment_system_created_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('engagement_assignment', models.OneToOneField(primary_key=True, serialize=False, to_field='id', to='engagement_assignment.EngagementAssignment')),
                ('recommended_action', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
