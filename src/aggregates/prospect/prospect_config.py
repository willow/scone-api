from django.apps import AppConfig

class ProspectConfig(AppConfig):
  name = 'src.aggregates.prospect'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.prospect.event_handlers
