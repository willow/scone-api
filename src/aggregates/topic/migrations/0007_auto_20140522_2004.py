# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0006_topic_snowball_stem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtopic',
            name='category_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'hashtag'), (2, 'subreddit')]),
        ),
    ]
