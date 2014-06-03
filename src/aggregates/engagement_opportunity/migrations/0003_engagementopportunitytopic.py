# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '__first__'),
        ('engagement_opportunity', '0002_neo_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngagementOpportunityTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('engagement_opportunity_topic_uid', models.CharField(max_length=100, unique=True)),
                ('engagement_opportunity', models.ForeignKey(to_field='id', to='engagement_opportunity.EngagementOpportunity')),
                ('topic_type', models.ForeignKey(to_field='id', to='topic.Topic')),
            ],
            options={
                'unique_together': set([('engagement_opportunity', 'topic_type')]),
            },
            bases=(models.Model,),
        ),
    ]
