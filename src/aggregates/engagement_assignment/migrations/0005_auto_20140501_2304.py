# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement_assignment', '0004_auto_20140501_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engagementassignment',
            name='score',
            field=models.DecimalField(max_digits=19, db_index=True, decimal_places=7),
        ),
    ]
