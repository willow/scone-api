from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=[
    'profile_uid', 'prospect_id', 'profile_name', 'profile_attrs', 'provider_type',
    'system_created_date',
  ]
)
