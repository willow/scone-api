from src.libs.common_domain.models import RevisionEvent
from src.libs.python_utils.types.type_utils import load_object
import json


def replay_events():
  rev_events = RevisionEvent.objects.order_by("pk")
  for rev_event in rev_events:
    signal = load_object(rev_event.name)

    # the aggregate will be the last item in the list
    obj = list(rev_event.revision.version_set.all())[-1].object

    data = json.loads(rev_event.data)
    data['instance'] = obj

    signal.send(obj.__class__, **data)

