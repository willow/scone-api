# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20140422_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='client_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'tech startup'), (2, 'author')], default=0),
            preserve_default=False,
        ),
    ]
