# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedProspect',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('client_uid', models.CharField(max_length=100)),
                ('prospect_uid', models.CharField(max_length=100)),
                ('system_created_date', models.DateTimeField()),
            ],
            options={
                'unique_together': set([('client_uid', 'prospect_uid')]),
            },
            bases=(models.Model,),
        ),
    ]
