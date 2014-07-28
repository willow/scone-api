from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['engagement_opportunity_uid', 'engagement_opportunity_external_id',
                  'engagement_opportunity_attrs', 'profile_id', 'provider_type', 'created_date', 'system_created_date']
)

added_topic = EventSignal(
  'added_topic', __name__, 1,
  providing_args=['engagement_opportunity_uid', 'engagement_opportunity_topic_uid', 'topic_type_id']
)
