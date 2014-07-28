from django.apps import AppConfig

class TopicConfig(AppConfig):
  name = 'src.aggregates.topic'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.aggregates.topic.event_handlers
