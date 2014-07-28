from celery import shared_task
import logging
from src.apps.graph.engagement_opportunity.services import engagement_opportunity_graph_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=180)
def create_engagement_opportunity_in_graphdb_task(self, engagement_opportunity_uid, profile_uid):
  log_message = (
    "Add eo to graphdb. eo_uid: %s, profile_uid: %s",
    engagement_opportunity_uid, profile_uid
  )

  try:
    with log_wrapper(logger.debug, *log_message):
      return engagement_opportunity_graph_service.create_engagement_opportunity_in_graphdb(
        engagement_opportunity_uid,
        profile_uid
      )['engagement_opportunity_uid']
  except Exception as e:

    ex = Exception(
      "Error creating eo. eo_uid: %s profile_uid: %s" %
      (engagement_opportunity_uid, profile_uid)
    ).with_traceback(e.__traceback__)

    logger.debug(ex, exc_info=True)

    self.retry(exc=ex)


@shared_task(bind=True, max_retries=3, default_retry_delay=180)
def add_topic_to_engagement_opportunity_in_graphdb_task(self, engagement_opportunity_uid,
                                                        engagement_opportunity_topic_uid,
                                                        topic_uid):
  log_message = (
    "Add topic to eo in graphdb. eo_uid: %s, eo_topic_uid: %s, topic_uid: %s",
    engagement_opportunity_uid, engagement_opportunity_topic_uid, topic_uid
  )

  try:
    with log_wrapper(logger.debug, *log_message):
      return engagement_opportunity_graph_service.add_topic_to_engagement_opportunity_in_graphdb(
        engagement_opportunity_uid,
        engagement_opportunity_topic_uid,
        topic_uid
      )['engagement_opportunity_topic_uid']
  except Exception as e:
    # this can happen in the admin screen. Example: we add a topic and then sub topics. The Sub-topic tasks runs
    # before the main parent topic even runs. We should wait until the main topic runs, then re-do this task in that
    # case.

    ex = Exception(
      "Error creating eo topic. eo_uid: %s eo_topic_uid: %s topic_uid: %s" %
      (engagement_opportunity_uid, engagement_opportunity_topic_uid, topic_uid)
    ).with_traceback(e.__traceback__)

    logger.debug(ex, exc_info=True)

    self.retry(exc=ex)
