from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['topic_uid', 'topic_name', 'system_name', 'snowball_stem']
)

deleted = EventSignal(
  'deleted', __name__, 1,
  providing_args=['topic_uid']
)

added_subtopic = EventSignal(
  'added_subtopic', __name__, 1,
  providing_args=['topic_uid', 'subtopic_uid', 'subtopic_name', 'subtopic_category', 'subtopic_attrs']
)

removed_subtopic = EventSignal(
  'removed_subtopic', __name__, 1,
  providing_args=['topic_uid', 'subtopic_uid']
)

updated_attrs = EventSignal(
  'updated_attrs', __name__, 1,
  providing_args=['topic_uid', 'topic_attrs']
)
