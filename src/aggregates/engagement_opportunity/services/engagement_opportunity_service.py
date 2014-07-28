from src.aggregates.engagement_opportunity import factories
from src.aggregates.engagement_opportunity.models import EngagementOpportunity
from src.libs.python_utils.logging.logging_utils import log_wrapper
from src.libs.web_utils.url import url_utils
import logging

logger = logging.getLogger(__name__)


def save_or_update(engagement_opportunity):
  engagement_opportunity.save(internal=True)


def get_engagement_opportunity_from_engagement_discovery(profile, engagement_opportunity_discovery_object,
                                                         _url_utils=url_utils):
  try:
    engagement_opportunity = get_engagement_opportunity_from_provider_info(
      engagement_opportunity_discovery_object.engagement_opportunity_external_id,
      engagement_opportunity_discovery_object.provider_type
    )

  except EngagementOpportunity.DoesNotExist:
    websites = engagement_opportunity_discovery_object.engagement_opportunity_attrs.get('websites')

    if websites:
      websites = [x for x in websites if x]

      websites_log_message = (
        "Get websites for eo_external_id: %s, websites: %s",
        engagement_opportunity_discovery_object.engagement_opportunity_external_id, websites
      )

      with log_wrapper(logger.debug, *websites_log_message):
        websites = _url_utils.get_unique_urls_from_iterable(websites)
        websites = _url_utils.summarize_websites_from_iterable(websites)

        # it's possible these websites all failed and didn't get summarzied
        if websites:
          engagement_opportunity_discovery_object.engagement_opportunity_attrs['websites'] = websites
        else:
          del engagement_opportunity_discovery_object.engagement_opportunity_attrs['websites']

    engagement_opportunity = factories.construct_engagement_opportunity_from_discovery(
      profile, engagement_opportunity_discovery_object
    )

    save_or_update(engagement_opportunity)

  return engagement_opportunity


def get_engagement_opportunity_from_provider_info(engagement_opportunity_external_id, provider_type):
  return EngagementOpportunity.objects.get(
    engagement_opportunity_external_id=engagement_opportunity_external_id, provider_type=provider_type
  )


def get_engagement_opportunity_from_uid(engagement_opportunity_uid):
  return EngagementOpportunity.objects.get(engagement_opportunity_uid=engagement_opportunity_uid)


def get_engagement_opportunity(engagement_opportunity_id):
  return EngagementOpportunity.objects.get(pk=engagement_opportunity_id)


def add_topic_to_engagement_opportunity(engagement_opportunity, topic):
  if not engagement_opportunity.topics.filter(topic_type=topic).exists():
    engagement_opportunity.associate_with_topic(topic)
    save_or_update(engagement_opportunity)

  return engagement_opportunity
