from django.apps import AppConfig

class ClientConfig(AppConfig):
  name = 'src.aggregates.client'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.client.event_handlers
    import src.aggregates.client.reversions
