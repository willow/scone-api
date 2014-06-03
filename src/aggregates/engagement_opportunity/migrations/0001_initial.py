# encoding: utf8
from django.db import models, migrations
import jsonfield.fields
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngagementOpportunity',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('engagement_opportunity_uid', models.CharField(max_length=100, unique=True)),
                ('engagement_opportunity_external_id', models.CharField(max_length=2400, db_index=True)),
                ('engagement_opportunity_attrs', jsonfield.fields.JSONField(blank=True, null=True)),
                ('profile', models.ForeignKey(to_field='id', to='profile.Profile')),
                ('provider_type', models.PositiveSmallIntegerField(choices=[(1, 'Twitter')])),
            ],
            options={
                'unique_together': set([('engagement_opportunity_external_id', 'provider_type')]),
            },
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
