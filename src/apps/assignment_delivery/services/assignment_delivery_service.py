from src.apps.assignment_delivery import constants
from src.apps.assignment_delivery.delivery_data_providers.reddit_delivery_data_provider import \
  RedditDeliveryDataProvider
from src.apps.assignment_delivery.delivery_data_providers.twitter_delivery_data_provider import \
  TwitterDeliveryDataProvider
from src.apps.engagement_discovery.enums import ProviderEnum
from src.libs.drive_utils.services import drive_service

_col_names = (
  "Profile", "Name", "Why they're in target audience", "Action they recently took", "Recommendation",
  "Followers", "Following"
)


def write_assignments_to_drive_for_client(client, _drive_service=drive_service):
  # get the best, recent assignments
  assignments = client.assignments.all().order_by("-score")[:50]

  rows = []

  for assignment in assignments:
    data_provider = _get_data_provider(assignment)
    assignment_data = data_provider.provide_delivery_data(assignment)
    rows.append(
      (
        assignment_data[constants.USERNAME],
        assignment_data[constants.NAME],
        assignment_data[constants.BIO],
        assignment_data[constants.ENGAGEMENT_OPPORTUNITY_URL],
        assignment_data[constants.RECOMMENDATION],
        assignment_data[constants.FOLLOWERS_COUNT],
        assignment_data[constants.FOLLOWING_COUNT],
      ),
    )

  _drive_service.write_new_worksheet_data_to_spreadsheet(client.client_name, _col_names, rows)


def _get_data_provider(engagement_assignment):
  if engagement_assignment.engagement_opportunity.provider_type == ProviderEnum.twitter:
    return TwitterDeliveryDataProvider()
  elif engagement_assignment.engagement_opportunity.provider_type == ProviderEnum.reddit:
    return RedditDeliveryDataProvider()
  else:
    return Exception("Invalid assignment type")
