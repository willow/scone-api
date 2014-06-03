# encoding: utf8
from django.db import migrations
from src.libs.graphdb_utils.services import graphdb_provider


def add_neo_index(models, schema_editor):
  graph_db = graphdb_provider.get_graph_client()
  graph_db.query("CREATE CONSTRAINT ON (client:Client) ASSERT client.client_uid IS UNIQUE")


def drop_neo_index(models, schema_editor):
  graph_db = graphdb_provider.get_graph_client()
  graph_db.query("DROP CONSTRAINT ON (client:Client) ASSERT client.client_uid IS UNIQUE")


class Migration(migrations.Migration):
  dependencies = [
    ('client', '0001_initial'),
  ]

  operations = [
    migrations.RunPython(add_neo_index, drop_neo_index),
  ]
