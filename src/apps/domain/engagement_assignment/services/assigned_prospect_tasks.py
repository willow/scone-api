from celery import shared_task
from src.aggregates.engagement_assignment.services import engagement_assignment_service
from src.apps.domain.engagement_assignment.services import assigned_prospect_service
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@shared_task
def update_assigned_prospect_task(engagement_assignment_uid, system_created_date):
  ea = engagement_assignment_service.get_engagement_assignments_by_uid(engagement_assignment_uid)

  return assigned_prospect_service.update_assigned_prospect(ea, system_created_date).id
