from django.db import models, transaction
from jsonfield import JSONField

import uuid

from src.aggregates.prospect.signals import created, updated_attrs
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event
from src.libs.django_utils.serialization.flexible_json_serializer import JSONSerializer


class Prospect(models.Model, AggregateBase):
  prospect_uid = models.CharField(max_length=100, unique=True)
  prospect_attrs = JSONField()


  @classmethod
  def _from_attrs(cls, prospect_attrs):
    ret_val = cls()

    ret_val._raise_event(
      created,
      prospect_uid=str(uuid.uuid1()),
      prospect_attrs=prospect_attrs,
    )

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.prospect_uid = kwargs['prospect_uid']
    self.prospect_attrs = kwargs['prospect_attrs']

  def update_attrs(self, attrs):
    if not isinstance(attrs, dict):
      raise TypeError("attrs must be a dict")

    self._raise_event(updated_attrs, prospect_attrs=attrs)

  def _handle_updated_attrs_event(self, **kwargs):
    prospect_attrs = kwargs['prospect_attrs']

    if self.prospect_attrs:
      self.prospect_attrs.update(prospect_attrs)
    else:
      self.prospect_attrs = prospect_attrs

  def __str__(self):
    return 'Prospect #' + str(self.pk) + ': ' + self.prospect_uid

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      self.send_events()
    else:
      from src.aggregates.prospect.services import prospect_service

      prospect_service.save_or_update(self)
