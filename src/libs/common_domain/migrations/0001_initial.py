# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reversion', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='RevisionEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.ForeignKey(to='reversion.Revision', to_field='id')),
                ('version', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=1024)),
                ('data', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
