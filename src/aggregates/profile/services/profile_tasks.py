from celery import shared_task
import logging

from src.aggregates.profile.services import profile_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@shared_task
def save_profile_from_provider_info_task(prospect_id, profile_external_id, provider_type, kwargs=None):
  log_message = (
    "Saving profile for prospect_id: %s, profile_external_id: %s, provider_type: %s",
    prospect_id, profile_external_id, provider_type
  )

  if not kwargs: kwargs = {}

  with log_wrapper(logger.debug, *log_message):
    ret_val = profile_service.save_profile_from_provider_info(
      prospect_id, profile_external_id, provider_type, **kwargs
    ).id

  return ret_val
