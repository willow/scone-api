from functools import partial
from unittest.mock import MagicMock
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.event_record import EventRecord
from src.libs.common_domain.event_signal import EventSignal


class DummyAggregate(AggregateBase):
  pass


def test_aggregate_base_sends_event_in_order():
  results = []

  def side_effect(signal_num, *ignore_me):
    results.append(signal_num)

  aggregate_test = DummyAggregate()

  signal1 = MagicMock(spec=EventRecord)
  signal1.event_obj.send = MagicMock(side_effect=partial(side_effect, 1))
  signal2 = MagicMock(spec=EventRecord)
  signal2.event_obj.send = MagicMock(side_effect=partial(side_effect, 2))

  aggregate_test._uncommitted_events.append(signal1)
  aggregate_test._uncommitted_events.append(signal2)

  aggregate_test.send_events()

  assert results == [1, 2]


def test_aggregate_uses_correct_naming_convention_when_applying():
  aggregate_test = DummyAggregate()

  event = MagicMock(spec=EventSignal)
  event.name = 'test'

  aggregate_test._handle_test_event = MagicMock()

  aggregate_test._apply_event(event)

  aggregate_test._handle_test_event.assert_called_with()
