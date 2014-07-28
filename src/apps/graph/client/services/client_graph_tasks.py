from celery import shared_task

from src.apps.graph.client.services import client_graph_service
import logging

logger = logging.getLogger(__name__)


@shared_task
def create_client_in_graphdb_task(client_uid):
  return client_graph_service.create_client_in_graphdb(client_uid)['client_uid']


@shared_task(bind=True, max_retries=3, default_retry_delay=180)
def create_ta_topic_in_graphdb_task(self, client_uid, ta_topic_uid, topic_uid):
  try:
    return client_graph_service.create_ta_topic_in_graphdb(client_uid, ta_topic_uid, topic_uid)['ta_topic_uid']
  except Exception as e:
    # this can happen in the admin screen. Example: we add a topic and then sub topics. The Sub-topic tasks runs
    # before the main parent topic even runs. We should wait until the main topic runs, then re-do this task in that
    # case.
    ex = Exception(
      "Error creating ta topic. client_uid: %s ta_topic_uid: %s topic_uid: %s" %
      (client_uid, ta_topic_uid, topic_uid,)
    ).with_traceback(e.__traceback__)

    logger.debug(ex, exc_info=True)

    self.retry(exc=ex)


@shared_task(bind=True, max_retries=3, default_retry_delay=180)
def delete_client_in_graphdb_task(self, client_uid):
  try:
    return client_graph_service.delete_client_in_graphdb(client_uid)
  except Exception as e:
    logger.debug(e, exc_info=True)
    self.retry(exc=e)


@shared_task(bind=True, max_retries=3, default_retry_delay=180)
def delete_ta_topic_in_graphdb_task(self, client_uid, ta_topic_uid):
  try:
    return client_graph_service.delete_ta_topic_in_graphdb(client_uid, ta_topic_uid)
  except Exception as e:
    logger.debug(e, exc_info=True)
    self.retry(exc=e)
