from src.libs.common_domain.event_signal import EventSignal

created = EventSignal(
  'created', __name__, 1,
  providing_args=['prospect_uid', 'prospect_attrs']
)

updated_attrs = EventSignal(
  'updated_attrs', __name__, 1,
  providing_args=['prospect_attrs']
)
