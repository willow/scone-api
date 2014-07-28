from celery import shared_task
from src.apps.graph.topic.services import topic_graph_service
import logging

logger = logging.getLogger(__name__)


@shared_task
def create_topic_in_graphdb_task(topic_uid):
  return topic_graph_service.create_topic_in_graphdb(topic_uid)['topic_uid']


@shared_task(bind=True, max_retries=3, default_retry_delay=180)
def create_subtopic_in_graphdb_task(self, topic_uid, subtopic_uid):
  try:
    return topic_graph_service.create_subtopic_in_graphdb(topic_uid, subtopic_uid)['topic_uid']
  except Exception as e:
    # this can happen in the admin screen. Example: we add a topic and then sub topics. The Sub-topic tasks runs
    # before the main parent topic even runs. We should wait until the main topic runs, then re-do this task in that
    # case.

    ex = Exception(
      "Error creating subtopic. topic_uid: %s subtopic_uid: %s" %
      (topic_uid, subtopic_uid)
    ).with_traceback(e.__traceback__)

    logger.debug(ex, exc_info=True)
    self.retry(exc=ex)


@shared_task(bind=True, max_retries=3, default_retry_delay=180)
def delete_topic_in_graphdb_task(self, topic_uid):
  try:
    return topic_graph_service.delete_topic_in_graphdb(topic_uid)
  except Exception as e:
    logger.debug(e, exc_info=True)
    self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=180)
def remove_subtopic_in_graphdb_task(self, topic_uid, subtopic_uid):
  try:
    return topic_graph_service.delete_subtopic_in_graphdb(topic_uid, subtopic_uid)
  except Exception as e:
    logger.debug(e, exc_info=True)
    self.retry(exc=e)
