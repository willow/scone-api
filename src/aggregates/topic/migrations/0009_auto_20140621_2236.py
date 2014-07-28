# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0008_auto_20140611_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtopic',
            name='category_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'hashtag'), (2, 'subreddit'), (3, 'keywords'), (4, 'exact match')]),
        ),
    ]
