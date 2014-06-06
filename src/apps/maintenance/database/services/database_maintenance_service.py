from datetime import timedelta
from django.utils import timezone
from src.aggregates.engagement_opportunity.models import EngagementOpportunity


def purge_old_data():
  previous_days = timedelta(days=1)
  threshold = timezone.now() - previous_days
  EngagementOpportunity.objects.filter(system_created_date__lte=threshold).delete()
