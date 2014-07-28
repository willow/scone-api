from django.core.management.base import NoArgsCommand
from src.libs.common_domain import event_store
from src.libs.graphdb_utils.services import graphdb_provider
from src.libs.graphdb_utils.services.graphdb_service import purge_data


class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    graph_db = graphdb_provider.get_graph_client()
    purge_data(graph_db)
    event_store.replay_events()
