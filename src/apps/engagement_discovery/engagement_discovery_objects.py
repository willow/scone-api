from collections import namedtuple
from src.libs.datetime_utils.parsers.datetime_parser import get_datetime

EngagementOpportunityDiscoveryObject = namedtuple(
  'EngagementOpportunityDiscoveryObject',
  'profile_external_id engagement_opportunity_external_id engagement_opportunity_attrs created_date '
  'provider_type provider_action_type topic_type'
)


def deserialize_engagement_opportunity_discovery_object(discovery_object):
  if isinstance(discovery_object, dict):
    # celery will pass in a dict when it's async but in the case of CELERY_ALWAYS_EAGER (like testing) it will not be
    # serialized at all and will remain a namedtuple

    # we can assume this was serialized and now needs to be deserialized.
    created_date = discovery_object['created_date']
    discovery_object['created_date'] = get_datetime(created_date)

    discovery_object = EngagementOpportunityDiscoveryObject(
      **discovery_object
    )

  return discovery_object
