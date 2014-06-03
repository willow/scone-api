# encoding: utf8
from django.db import models, migrations
import jsonfield.fields
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headers', models.TextField(null=True, blank=True)),
                ('text', models.TextField(null=True, blank=True)),
                ('html', models.TextField(null=True, blank=True)),
                ('to', models.TextField()),
                ('from_address', models.TextField()),
                ('cc', models.TextField(null=True, blank=True)),
                ('subject', models.TextField(null=True, blank=True)),
                ('dkim', models.TextField(null=True, blank=True)),
                ('SPF', models.TextField(null=True, blank=True)),
                ('envelope', jsonfield.fields.JSONField(null=True, blank=True)),
                ('charsets', models.CharField(null=True, max_length=255, blank=True)),
                ('spam_score', models.FloatField(validators=[django.core.validators.MaxValueValidator(2.3)], null=True, blank=True)),
                ('spam_report', models.TextField(null=True, blank=True)),
                ('sender_ip', models.CharField(null=True, max_length=255, blank=True)),
                ('message_id', models.CharField(null=True, max_length=1024, blank=True)),
                ('in_reply_to_message_id', models.CharField(null=True, max_length=1024, blank=True)),
                ('email_direction', models.PositiveSmallIntegerField(max_length=2, choices=[(1, 'Incoming'), (2, 'Outgoing')])),
                ('sent_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', to_field='id', null=True, blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('changed_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': set([('message_id', 'sent_date')]),
            },
            bases=(models.Model,),
        ),
    ]
