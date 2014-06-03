# encoding: utf8
from django.db import models, migrations
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('client_uid', models.CharField(max_length=100, unique=True)),
                ('client_name', models.CharField(max_length=2400)),
            ],
            options={
            },
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
        migrations.CreateModel(
            name='TATopic',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('client', models.ForeignKey(to_field='id', to='client.Client')),
                ('topic_type', models.ForeignKey(to_field='id', to='topic.Topic')),
                ('ta_topic_uid', models.CharField(max_length=100, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
