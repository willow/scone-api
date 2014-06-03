# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0003_remove_topic_topic_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subtopic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('subtopic_uid', models.CharField(unique=True, max_length=100)),
                ('subtopic_name', models.CharField(max_length=2400)),
                ('topic', models.ForeignKey(to_field='id', to='topic.Topic')),
                ('category_type', models.PositiveSmallIntegerField(choices=[(1, 'hashtag')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='topic',
            name='system_name',
            field=models.CharField(unique=True, default=0, max_length=2004),
            preserve_default=False,
        ),
    ]
