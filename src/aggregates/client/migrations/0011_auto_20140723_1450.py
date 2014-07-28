# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_auto_20140722_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='enabled',
            field=models.BooleanField(default=None),
        ),
    ]
