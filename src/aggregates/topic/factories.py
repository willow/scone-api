from src.aggregates.topic.models import Topic


def create_topic(topic_name):
  topic = Topic._from_attrs(topic_name)
  return topic
