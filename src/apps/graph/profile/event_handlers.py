from django.dispatch import receiver

from src.aggregates.profile.signals import created
from src.aggregates.prospect.services import prospect_service
from src.aggregates.topic.services import topic_service
from src.apps.graph import constants
from src.apps.graph.profile.services import profile_graph_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(created)
def profile_created_callback(**kwargs):
  prospect_id = kwargs.pop('prospect_id')
  prospect_uid = prospect_service.get_prospect(prospect_id).prospect_uid

  task_kwargs = {}
  profile_attrs = kwargs['profile_attrs']
  profile_uid = kwargs['profile_uid']

  if profile_attrs:
    topic_ids = profile_attrs.get(constants.TOPIC_IDS)

    if topic_ids:
      topic_uids = [topic_service.get_topic(topic_id).topic_uid for topic_id in topic_ids]
      task_kwargs[constants.TOPIC_UIDS] = topic_uids

  profile_graph_tasks.create_profile_in_graphdb_task.delay(profile_uid, prospect_uid, task_kwargs)
