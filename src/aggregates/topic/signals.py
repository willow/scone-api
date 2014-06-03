from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['instance', 'topic_uid', 'topic_name', 'system_name', 'snowball_stem']
)

added_subtopic = EventSignal(
  'added_subtopic', __name__, 1,
  providing_args=['instance', 'subtopic_uid', 'subtopic_name', 'subtopic_category']
)
