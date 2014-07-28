from django.apps import AppConfig


class DomainConfig(AppConfig):
  name = 'src.apps.domain'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.domain.engagement_assignment.event_handlers
