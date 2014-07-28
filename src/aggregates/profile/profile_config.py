from django.apps import AppConfig

class ProfileConfig(AppConfig):
  name = 'src.aggregates.profile'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.profile.event_handlers
