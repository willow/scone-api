from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=[
    'instance', 'engagement_assignment_uid', 'client_id', 'engagement_opportunity_id', 'score', 'score_attrs',
    'recommended_action', 'system_created_date'
  ]
)
