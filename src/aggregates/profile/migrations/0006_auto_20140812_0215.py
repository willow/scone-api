# encoding: utf8
from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_auto_20140603_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_attrs',
            field=jsonfield.fields.JSONField(),
        ),
    ]
