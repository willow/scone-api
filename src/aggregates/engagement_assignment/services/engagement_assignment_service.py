from src.aggregates.engagement_assignment import factories
from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.models import EngagementAssignment
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service
from src.aggregates.prospect.services import prospect_service
from src.apps.graph.engagement_assignment.services import engagement_assignment_graph_service
import logging
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


def get_engagement_assignment(engagement_assignment_id):
  return EngagementAssignment.objects.get(id=engagement_assignment_id)


def save_or_update(engagement_assignment):
  engagement_assignment.save(internal=True)


def create_engagement_assignment(client, assignment_attrs):
  engagement_assignment = factories.create_engagement_assignment(client, assignment_attrs)
  save_or_update(engagement_assignment)
  return engagement_assignment


def get_grouped_entities_for_client(client):
  ret_val = []
  entity_groups_to_add = engagement_assignment_graph_service.get_grouped_entities_for_client(client.client_uid)

  for entity_group_to_add in entity_groups_to_add:
    prospect_uid = entity_group_to_add['prospect_uid']
    prospect = prospect_service.get_prospect_from_uid(prospect_uid)
    ea_group = {constants.PROSPECT_ID: prospect.id}

    eo_ids = []
    for eo_uid in entity_group_to_add['eo_uids']:
      eo = engagement_opportunity_service.get_engagement_opportunity_from_uid(eo_uid)
      eo_ids.append(eo.id)
    if eo_ids: ea_group[constants.ASSIGNED_EO_UIDS] = eo_ids

    profile_ids = []
    for profile_uid in entity_group_to_add['profile_uids']:
      profile = profile_service.get_profile_from_uid(profile_uid)
      profile_ids.append(profile.id)
    if profile_ids: ea_group[constants.ASSIGNED_PROFILE_UIDS] = profile_ids

    ret_val.append(ea_group)

  return ret_val


def refresh_assignments(client):
  method_log_message = (
    "Refresh assignments for client: %s",
    client
  )

  with log_wrapper(logger.debug, *method_log_message):

    counter = 1

    entities_to_add = get_grouped_entities_for_client(client)

    total_assignments_count = len(entities_to_add)

    logger.debug("Assignments to create for %s: %i", client, total_assignments_count)

    for group in entities_to_add:
      group_log_message = ("Assignment: %i out of %i for client: %s", counter, total_assignments_count, client)

      with log_wrapper(logger.debug, *group_log_message):

        assignment_attrs = {}

        eo_ids = group.get(constants.ASSIGNED_EO_UIDS)
        if eo_ids: assignment_attrs[constants.ASSIGNED_EO_UIDS] = eo_ids

        profile_ids = group.get(constants.ASSIGNED_PROFILE_UIDS)
        if profile_ids: assignment_attrs[constants.ASSIGNED_PROFILE_UIDS] = profile_ids

        try:
          create_engagement_assignment(client, assignment_attrs)
        except:
          logger.warn("Error creating assignment", exc_info=True)

        counter += 1


def get_engagement_assignments_by_score(engagement_assignment_ids):
  return EngagementAssignment.objects.filter(id__in=engagement_assignment_ids).order_by("-score")


def get_engagement_assignments_by_uid(engagement_assignment_uid):
  return EngagementAssignment.objects.get(engagement_assignment_uid=engagement_assignment_uid)
