from django.apps import AppConfig

class profileConfig(AppConfig):
  name = 'src.aggregates.profile'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.profile.event_handlers
    import src.aggregates.profile.reversions
