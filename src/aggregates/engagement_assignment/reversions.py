import reversion
from src.aggregates.engagement_assignment.models import EngagementAssignment, Recommendation


reversion.register(EngagementAssignment, follow=['recommendation'])
reversion.register(Recommendation)
