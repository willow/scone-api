# encoding: utf8
from django.db import models, migrations
import jsonfield.fields
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prospect',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('prospect_uid', models.CharField(max_length=100, unique=True)),
                ('prospect_attrs', jsonfield.fields.JSONField(blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
