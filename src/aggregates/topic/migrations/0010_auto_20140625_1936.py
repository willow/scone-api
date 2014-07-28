# encoding: utf8
from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0009_auto_20140621_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtopic',
            name='category_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'twitter search'), (2, 'subreddit'), (3, 'keywords')]),
        ),
    ]
