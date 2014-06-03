from celery import shared_task
from src.apps.graph.topic.services import topic_graph_service


@shared_task
def create_topic_in_graphdb_task(topic_uid):
  return topic_graph_service.create_topic_in_graphdb(topic_uid)['topic_uid']


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def create_subtopic_in_graphdb_task(self, topic_uid, subtopic_uid):
  try:
    return topic_graph_service.create_subtopic_in_graphdb(topic_uid, subtopic_uid)['topic_uid']
  except Exception as e:
    # this can happen in the admin screen. Example: we add a topic and then sub topics. The Sub-topic tasks runs
    # before the main parent topic even runs. We should wait until the main topic runs, then re-do this task in that
    # case.
    self.retry(exc=e)

