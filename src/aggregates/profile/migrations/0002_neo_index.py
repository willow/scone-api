# encoding: utf8
from django.db import migrations
from src.libs.graphdb_utils.services import graphdb_provider


def add_eo_index(models, schema_editor):
  graph_db = graphdb_provider.get_graph_client()
  graph_db.query("CREATE CONSTRAINT ON (profile:Profile) ASSERT profile.profile_uid IS UNIQUE")


def drop_eo_index(models, schema_editor):
  graph_db = graphdb_provider.get_graph_client()
  graph_db.query("DROP CONSTRAINT ON (profile:Profile) ASSERT profile.profile_uid IS UNIQUE")


class Migration(migrations.Migration):
  dependencies = [
    ('profile', '0001_initial'),
  ]

  operations = [
    migrations.RunPython(add_eo_index, drop_eo_index),
  ]
