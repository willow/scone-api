from django.dispatch import receiver

from src.aggregates.topic.signals import created, added_subtopic
from src.aggregates.topic.models import Topic
from src.apps.graph.topic.services import topic_graph_tasks


@receiver(created, sender=Topic)
def topic_created_callback(**kwargs):
  topic_graph_tasks.create_topic_in_graphdb_task.delay(kwargs['instance'].topic_uid)


@receiver(added_subtopic, sender=Topic)
def subtopic_created_callback(**kwargs):
  topic_graph_tasks.create_subtopic_in_graphdb_task.delay(kwargs['instance'].topic_uid, kwargs['subtopic_uid'])
