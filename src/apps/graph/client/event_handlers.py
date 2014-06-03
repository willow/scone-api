from django.dispatch import receiver

from src.aggregates.client.signals import created, added_ta_topic
from src.aggregates.client.models import Client
from src.aggregates.topic.services import topic_service
from src.apps.graph.client.services import client_graph_tasks


@receiver(created, sender=Client)
def client_created_callback(**kwargs):
  client_graph_tasks.create_client_in_graphdb_task.delay(kwargs['instance'].client_uid)

@receiver(added_ta_topic, sender=Client)
def added_ta_topic_callback(**kwargs):
  ta_topic_uid = kwargs.pop('ta_topic_uid')
  topic_id = kwargs.pop('topic_type_id')
  
  topic_uid = topic_service.get_topic(topic_id).topic_uid
  
  client_graph_tasks.create_ta_topic_in_graphdb_task.delay(kwargs['instance'].client_uid, ta_topic_uid, topic_uid)
