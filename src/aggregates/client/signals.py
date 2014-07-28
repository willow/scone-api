from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['client_uid', 'client_name', 'client_type']
)

added_ta_topic = EventSignal(
  'added_ta_topic', __name__, 1,
  providing_args=['client_uid', 'ta_topic_uid', 'topic_type_id']
)

removed_ta_topic = EventSignal(
  'removed_ta_topic', __name__, 1,
  providing_args=['client_uid', 'ta_topic_uid']
)

deleted = EventSignal(
  'deleted', __name__, 1,
  providing_args=['client_uid']
)

disabled = EventSignal(
  'disabled', __name__, 1,
  providing_args=['client_uid']
)

enabled = EventSignal(
  'enabled', __name__, 1,
  providing_args=['client_uid']
)
