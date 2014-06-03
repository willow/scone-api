# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0005_neo_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='snowball_stem',
            field=models.CharField(max_length=2400, default=0),
            preserve_default=False,
        ),
    ]
