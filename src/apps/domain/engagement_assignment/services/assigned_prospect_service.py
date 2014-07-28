from dateutil.relativedelta import relativedelta
from django.utils import timezone
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service
from src.apps.domain.engagement_assignment.models import AssignedProspect
from src.apps.domain import constants


def save_or_update(assigned_prospect):
  assigned_prospect.save(internal=True)


def update_assigned_prospect(engagement_assignment, system_created_date):
  client_uid = engagement_assignment.client.client_uid
  entity_type, assigned_entity_ids = list(engagement_assignment.assignment_attrs.items())[0]
  assigned_entity_id = assigned_entity_ids[0]

  if entity_type == constants.ASSIGNED_EO_IDS:
    assigned_entity = engagement_opportunity_service.get_engagement_opportunity(assigned_entity_id)
    prospect_uid = assigned_entity.profile.prospect.prospect_uid
  elif entity_type == constants.ASSIGNED_PROFILE_IDS:
    assigned_entity = profile_service.get_profile(assigned_entity_id)
    prospect_uid = assigned_entity.prospect.prospect_uid
  else:
    raise ValueError("Invalid assignment attrs")

  try:
    ap = get_assigned_prospect_from_attrs(client_uid, prospect_uid)
  except AssignedProspect.DoesNotExist:
    ap = AssignedProspect(client_uid=client_uid, prospect_uid=prospect_uid)

  ap.system_created_date = system_created_date

  save_or_update(ap)

  return ap


def _get_assigned_prospect_from_attrs_queryset(client_uid, prospect_uid):
  return AssignedProspect.objects.filter(client_uid=client_uid, prospect_uid=prospect_uid)


def get_assigned_prospect_from_attrs(client_uid, prospect_uid):
  return _get_assigned_prospect_from_attrs_queryset(client_uid, prospect_uid).get()


def get_recently_assigned_prospect_from_attrs(client_uid, prospect_uid):
  delta = timezone.now() - relativedelta(months=3)

  return (
    _get_assigned_prospect_from_attrs_queryset(client_uid, prospect_uid)
    .filter(system_created_date__gte=delta)
    .get()
  )
