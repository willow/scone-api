# encoding: utf8
from django.db import models, migrations
import jsonfield.fields
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('profile_uid', models.CharField(max_length=100, unique=True)),
                ('profile_external_id', models.CharField(max_length=2400)),
                ('profile_attrs', jsonfield.fields.JSONField(blank=True, null=True)),
                ('provider_type', models.PositiveSmallIntegerField(choices=[(1, 'Twitter')])),
            ],
            options={
                'unique_together': set([('profile_external_id', 'provider_type')]),
            },
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
