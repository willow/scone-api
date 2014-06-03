from celery import shared_task

from src.apps.graph.client.services import client_graph_service


@shared_task
def create_client_in_graphdb_task(client_uid):
  return client_graph_service.create_client_in_graphdb(client_uid)['client_uid']


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def create_ta_topic_in_graphdb_task(self, client_uid, ta_topic_uid, topic_uid):
  try:
    return client_graph_service.create_ta_topic_in_graphdb(client_uid, ta_topic_uid, topic_uid)['ta_topic_uid']
  except Exception as e:
    # this can happen in the admin screen. Example: we add a topic and then sub topics. The Sub-topic tasks runs
    # before the main parent topic even runs. We should wait until the main topic runs, then re-do this task in that
    # case.
    self.retry(exc=e)
