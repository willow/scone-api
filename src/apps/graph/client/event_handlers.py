from django.dispatch import receiver

from src.aggregates.client.signals import created, added_ta_topic, deleted, removed_ta_topic
from src.aggregates.topic.services import topic_service
from src.apps.graph.client.services import client_graph_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(created)
def client_created_callback(**kwargs):
  client_graph_tasks.create_client_in_graphdb_task.delay(kwargs['client_uid'])

@event_idempotent
@receiver(deleted)
def client_deleted_callback(**kwargs):
  client_graph_tasks.delete_client_in_graphdb_task.delay(kwargs['client_uid'])

@event_idempotent
@receiver(added_ta_topic)
def added_ta_topic_callback(**kwargs):
  ta_topic_uid = kwargs.pop('ta_topic_uid')
  topic_id = kwargs.pop('topic_type_id')
  
  topic_uid = topic_service.get_topic(topic_id).topic_uid
  
  client_graph_tasks.create_ta_topic_in_graphdb_task.delay(kwargs['client_uid'], ta_topic_uid, topic_uid)

@event_idempotent
@receiver(removed_ta_topic)
def removed_ta_topic_callback(**kwargs):
  client_uid = kwargs.pop('client_uid')
  ta_topic_uid = kwargs.pop('ta_topic_uid')

  client_graph_tasks.delete_ta_topic_in_graphdb_task.delay(client_uid, ta_topic_uid)
