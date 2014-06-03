from django.dispatch import receiver
from src.aggregates.client.models import Client
from src.aggregates.client.signals import assigned_engagement_opportunity
from src.aggregates.engagement_assignment.services import engagement_assignment_tasks


@receiver(assigned_engagement_opportunity, sender=Client)
def assigned_engagement_opportunity_callback(**kwargs):
  engagement_opportunity_id = kwargs.pop('engagement_opportunity_id')
  engagement_assignment_tasks.create_engagement_assignment_task.delay(
    kwargs['instance'].id,
    engagement_opportunity_id
  )
