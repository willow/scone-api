# encoding: utf8
from django.db import migrations
from src.libs.graphdb_utils.services import graphdb_provider


def add_ea_index(models, schema_editor):
  graph_db = graphdb_provider.get_graph_client()
  graph_db.query("CREATE CONSTRAINT ON (ea:EngagementAssignment) ASSERT ea.engagement_assignment_uid IS UNIQUE")


def drop_ea_index(models, schema_editor):
  graph_db = graphdb_provider.get_graph_client()
  graph_db.query("DROP CONSTRAINT ON (ea:EngagementAssignment) ASSERT ea.engagement_assignment_uid IS UNIQUE")


class Migration(migrations.Migration):
  dependencies = [
    ('engagement_assignment', '0001_initial'),
  ]

  operations = [
    migrations.RunPython(add_ea_index, drop_ea_index),
  ]
