import reversion

from src.aggregates.engagement_opportunity.models import EngagementOpportunity, EngagementOpportunityTopic


reversion.register(EngagementOpportunity, follow=['topics'])
reversion.register(EngagementOpportunityTopic)
