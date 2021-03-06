from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=[
    'engagement_assignment_uid', 'client_id', 'assignment_attrs', 'score', 'score_attrs',
    'recommended_action', 'system_created_date'
  ]
)

delivered = EventSignal(
  'delivered', __name__, 1,
  providing_args=[
    'engagement_assignment_uid', 'system_created_date'
  ]
)
