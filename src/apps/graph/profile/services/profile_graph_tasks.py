from celery import shared_task
import logging
from src.apps.graph.profile.services import profile_graph_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=180)
def create_profile_in_graphdb_task(self, profile_uid, prospect_uid, kwargs=None):
  if not kwargs: kwargs = {}

  log_message = (
    "Create profile in graphdb task for profile_uid: %s, prospect_uid: %s",
    profile_uid, prospect_uid
  )

  try:
    with log_wrapper(logger.debug, *log_message):
      return profile_graph_service.create_profile_in_graphdb(profile_uid, prospect_uid, **kwargs)['profile_uid']
  except Exception as e:
    # this can happen in the admin screen. Example: we add a topic and then sub topics. The Sub-topic tasks runs
    # before the main parent topic even runs. We should wait until the main topic runs, then re-do this task in that
    # case.

    ex = Exception(
      "Error creating profile. profile_uid: %s prospect_uid: %s" %
      (profile_uid, prospect_uid)
    ).with_traceback(e.__traceback__)

    logger.debug(ex, exc_info=True)

    self.retry(exc=ex)
