# encoding: utf8
from django.db import models, migrations
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_opportunity', '__first__'),
        ('client', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngagementAssignment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('engagement_assignment_uid', models.CharField(db_index=True, max_length=2400)),
                ('client', models.ForeignKey(to='client.Client', to_field='id')),
                ('engagement_opportunity', models.ForeignKey(to='engagement_opportunity.EngagementOpportunity', to_field='id')),
            ],
            options={
                'unique_together': set([('client', 'engagement_opportunity')]),
            },
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
