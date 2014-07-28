from django.dispatch import receiver

from src.aggregates.topic.signals import created, added_subtopic, deleted, removed_subtopic
from src.apps.graph.topic.services import topic_graph_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(created)
def topic_created_callback(**kwargs):
  topic_graph_tasks.create_topic_in_graphdb_task.delay(kwargs['topic_uid'])

@event_idempotent
@receiver(deleted)
def topic_deleted_callback(**kwargs):
  topic_graph_tasks.delete_topic_in_graphdb_task.delay(kwargs['topic_uid'])


@event_idempotent
@receiver(added_subtopic)
def subtopic_created_callback(**kwargs):
  topic_graph_tasks.create_subtopic_in_graphdb_task.delay(kwargs['topic_uid'], kwargs['subtopic_uid'])

@event_idempotent
@receiver(removed_subtopic)
def subtopic_removed_callback(**kwargs):
  topic_graph_tasks.remove_subtopic_in_graphdb_task.delay(kwargs['topic_uid'], kwargs['subtopic_uid'])
