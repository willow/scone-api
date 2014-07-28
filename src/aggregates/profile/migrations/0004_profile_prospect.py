# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_auto_20140522_2004'),
        ('prospect', '0002_neo_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='prospect',
            field=models.ForeignKey(to='prospect.Prospect', to_field='id', default=0),
            preserve_default=False,
        ),
    ]
