# encoding: utf8
from django.db import models, migrations
import jsonfield.fields


def update_func(models, schema_editor):
  Profile = models.get_model("profile", "Profile")
  Profile.objects.filter(profile_attrs=None).update(profile_attrs={})


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_auto_20140603_2239'),
    ]

    operations = [
      migrations.RunPython(update_func),
        migrations.AlterField(
            model_name='profile',
            name='profile_attrs',
            field=jsonfield.fields.JSONField(),
        ),
    ]
