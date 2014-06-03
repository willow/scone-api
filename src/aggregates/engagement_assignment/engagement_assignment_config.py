from django.apps import AppConfig

class EngagementAssignmentConfig(AppConfig):
  name = 'src.aggregates.engagement_assignment'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.engagement_assignment.event_handlers
    import src.aggregates.engagement_assignment.reversions
