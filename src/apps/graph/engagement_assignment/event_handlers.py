from django.dispatch import receiver
from src.aggregates.client.services import client_service
from src.aggregates.engagement_assignment.models import EngagementAssignment
from src.aggregates.engagement_assignment.signals import created
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service
from src.apps.graph import constants
from src.apps.graph.engagement_assignment.services import engagement_assignment_graph_tasks
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(created)
def engagement_assignment_created_callback(**kwargs):
  client_id = kwargs.pop('client_id')
  assignment_attrs = kwargs.pop('assignment_attrs')

  if constants.ASSIGNED_EO_IDS in assignment_attrs:

    eo_uids = []
    for eo_id in assignment_attrs[constants.ASSIGNED_EO_IDS]:
      eo = engagement_opportunity_service.get_engagement_opportunity(eo_id)
      eo_uids.append(eo.engagement_opportunity_uid)
    assignment_attrs[constants.ASSIGNED_EO_UIDS] = eo_uids
    del assignment_attrs[constants.ASSIGNED_EO_IDS]

  if constants.ASSIGNED_PROFILE_IDS in assignment_attrs:

    profile_uids = []
    for profile_id in assignment_attrs[constants.ASSIGNED_PROFILE_IDS]:
      profile = profile_service.get_profile(profile_id)
      profile_uids.append(profile.profile_uid)
    assignment_attrs[constants.ASSIGNED_PROFILE_UIDS] = profile_uids
    del assignment_attrs[constants.ASSIGNED_PROFILE_IDS]

  client_uid = client_service.get_client_from_id(client_id).client_uid

  engagement_assignment_graph_tasks.create_engagement_assignment_in_graphdb_task.delay(
    kwargs['engagement_assignment_uid'],
    client_uid,
    assignment_attrs
  )
