from src.aggregates.prospect.services import prospect_tasks
from django.dispatch import receiver
from src.aggregates.profile.signals import created
from src.libs.common_domain.decorators import event_idempotent


@receiver(created)
def profile_created_callback(**kwargs):
  prospect_id = kwargs['prospect_id']
  prospect_tasks.manage_prospect_profiles_task.delay(prospect_id)

@event_idempotent
@receiver(created)
def manage_prospect_attrs_created_callback(**kwargs):
  profile_uid = kwargs['profile_uid']
  prospect_tasks.manage_prospect_attrs_task.delay(profile_uid)
