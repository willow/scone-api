# encoding: utf8
from django.db import models, migrations
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('topic_uid', models.CharField(max_length=100, unique=True)),
                ('topic_name', models.CharField(max_length=2400)),
                ('topic_type', models.PositiveSmallIntegerField(db_index=True, choices=[(1, 'keyword')])),
            ],
            options={
            },
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
