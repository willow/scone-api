from src.libs.common_domain.models import Event
from src.libs.django_utils.query.query_utils import batch_qs
from src.libs.python_utils.types.type_utils import load_object
import logging

logger = logging.getLogger(__name__)


def replay_events():
  counter = 0
  rev_events = Event.objects.order_by("pk")
  logger.debug("Replay %i events", rev_events.count())

  for rev_event_batch in batch_qs(rev_events):
    logger.debug("starting batch : %s", rev_event_batch[0])

    rev_events = rev_event_batch[3]

    for rev_event in rev_events:
      signal = load_object(rev_event.name)

      data = rev_event.data

      try:
        signal.send(None, allow_non_idempotent=False, **data)
      except Exception:
        logger.warn("Error sending signal for: %s Data: %s", rev_event.name, data, exc_info=True)
      counter += 1
      logger.debug("Sending signal: %s : %i", rev_event.name, counter)
