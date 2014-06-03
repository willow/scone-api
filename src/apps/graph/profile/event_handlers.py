from django.dispatch import receiver

from src.aggregates.profile.signals import created
from src.aggregates.profile.models import Profile
from src.apps.graph.profile.services import profile_graph_tasks


@receiver(created, sender=Profile)
def profile_created_callback(**kwargs):
  profile_graph_tasks.create_profile_in_graphdb_task.delay(kwargs['instance'].profile_uid)
