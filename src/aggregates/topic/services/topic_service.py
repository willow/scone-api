from src.aggregates.topic import factories
from src.aggregates.topic.models import Topic, Subtopic
from src.libs.text_utils.stemming import stemming_utils


def create_topic(topic_name):
  topic = factories.create_topic(topic_name)
  save_or_update(topic)
  return topic


def update_attrs(topic, topic_attrs):
  topic.update_attrs(topic_attrs)
  save_or_update(topic)
  return topic


def save_or_update(topic):
  topic.save(internal=True)


def get_topic(pk):
  return Topic.objects.get(pk=pk)


def get_all_topics():
  return Topic.objects.select_related('subtopics').all()


def get_active_topics():
  # make sure to use `distinct` because child-filtering results in many rows being returned because of the inner-join
  return get_all_topics().filter(client_ta_topics__client__enabled=True).distinct()


def get_subtopic(subtopic_id):
  return Subtopic.objects.get(pk=subtopic_id)


def create_topic_stem(topic_name, _stem_service=stemming_utils):
  return _stem_service.find_stem(topic_name)


def delete_topic(topic):
  topic.delete(internal=True)
