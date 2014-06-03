from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['instance', 'client_uid', 'client_name', 'client_type']
)

added_ta_topic = EventSignal(
  'added_ta_topic', __name__, 1,
  providing_args=['instance', 'ta_topic_uid', 'topic_type_id']
)

assigned_engagement_opportunity = EventSignal(
  'assigned_engagement_opportunity', __name__, 1,
  providing_args=['instance', 'engagement_opportunity_id']
)
