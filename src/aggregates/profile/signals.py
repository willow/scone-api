from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['instance', 'profile_uid', 'profile_name', 'profile_attrs', 'provider_type']
)
