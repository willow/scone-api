# encoding: utf8
from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0007_auto_20140522_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtopic',
            name='subtopic_attrs',
            field=jsonfield.fields.JSONField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subtopic',
            name='category_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'hashtag'), (2, 'subreddit'), (3, 'keywords')]),
        ),
    ]
