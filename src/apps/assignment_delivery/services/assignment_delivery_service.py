from dateutil.relativedelta import relativedelta
from django.utils import timezone
from src.aggregates.engagement_assignment.services import engagement_assignment_service
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service
from src.aggregates.prospect.services import prospect_service
from src.apps.assignment_delivery import constants
from src.apps.assignment_delivery.delivery_data_providers.linkedin_delivery_data_provider import \
  LinkedinDeliveryDataProvider
from src.apps.assignment_delivery.delivery_data_providers.reddit_delivery_data_provider import \
  RedditDeliveryDataProvider
from src.apps.assignment_delivery.delivery_data_providers.twitter_delivery_data_provider import \
  TwitterDeliveryDataProvider
from src.apps.engagement_discovery.enums import ProviderEnum
from src.libs.drive_utils.services import drive_service

_col_names = (
  "Profile", "Name", "Why they're in target audience", "Action they recently took", "Followers", "Following", "Email",
  "Score", "Assignment Id"
)


def get_new_client_assignments(client):
  # get the best, recent assignments
  delta = timezone.now() - relativedelta(days=1)

  assignments = client.assignments.filter(system_created_date__gte=delta).order_by("-score")[:20]

  return assignments


def get_new_client_assignments_ids(client):
  return get_new_client_assignments(client).values_list("id", flat=True)


def prepare_assignment_for_delivery(assignment):
  attr = assignment.score_attrs[0]
  entity_id = attr[constants.ID]
  entity_type = attr[constants.ENTITY_TYPE]

  if entity_type == constants.EO:
    assigned_entity = engagement_opportunity_service.get_engagement_opportunity(entity_id)
    prospect = assigned_entity.profile.prospect
  elif entity_type == constants.PROFILE:
    assigned_entity = profile_service.get_profile(entity_id)
    prospect = assigned_entity.prospect
  else:
    raise ValueError("Invalid assignment attrs")

  #todo why is this method here?

def write_assignments_to_drive(assignments, client, _drive_service=drive_service):
  rows = []

  for assignment in assignments:
    assignment_attr = sorted(assignment.score_attrs, key=lambda x: x['score'], reverse=True)[0]

    entity_id = assignment_attr[constants.ID]
    entity_type = assignment_attr[constants.ENTITY_TYPE]

    if entity_type == constants.EO:
      assigned_entity = engagement_opportunity_service.get_engagement_opportunity(entity_id)
      provider_type = assigned_entity.provider_type
    elif entity_type == constants.PROFILE:
      assigned_entity = profile_service.get_profile(entity_id)
      provider_type = assigned_entity.provider_type
    else:
      raise ValueError("Invalid assignment attrs")

    data_provider = _get_data_provider(provider_type)
    assignment_data = data_provider.provide_delivery_data(assigned_entity)
    rows.append(
      (
        assignment_data[constants.USERNAME],
        assignment_data[constants.NAME],
        assignment_data[constants.BIO],
        assignment_data[constants.URL],
        assignment_data[constants.FOLLOWERS_COUNT],
        assignment_data[constants.FOLLOWING_COUNT],
        assignment_data[constants.EMAIL_ADDRESSES],
        assignment.score,
        assignment.id,
      ),
    )

  _drive_service.write_new_worksheet_data_to_spreadsheet(client.client_name, _col_names, rows)

  # mark the first 7 as `delivered`. This is quite an arbitrary number, and the ideal scenario would be that when
  # these are truly delivered (email, spreadsheet, etc), then those are marked as delivered. However, for the time
  # being, we'll just assume the first 10 assignments were delivered even if we only email 5/10 of them.
  for assignment in assignments[:10]:
    assignment.deliver()
    engagement_assignment_service.save_or_update(assignment)

def _get_data_provider(provider_type):
  if provider_type == ProviderEnum.twitter:
    return TwitterDeliveryDataProvider()
  elif provider_type == ProviderEnum.reddit:
    return RedditDeliveryDataProvider()
  elif provider_type == ProviderEnum.linkedin:
    return LinkedinDeliveryDataProvider()
  else:
    return Exception("Invalid assignment type")
