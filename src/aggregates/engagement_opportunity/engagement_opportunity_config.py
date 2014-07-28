from django.apps import AppConfig

class EngagementOpportunityConfig(AppConfig):
  name = 'src.aggregates.engagement_opportunity'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.engagement_opportunity.event_handlers
