from django.dispatch import receiver

from src.aggregates.prospect.signals import created
from src.apps.graph.prospect.services import prospect_graph_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(created)
def profile_created_callback(**kwargs):
  prospect_graph_tasks.create_prospect_in_graphdb_task.delay(kwargs['prospect_uid'])
