from django.db import models, transaction
from django.utils import timezone
from jsonfield import JSONField
import uuid

from src.aggregates.profile.signals import created
from src.apps.engagement_discovery.enums import ProviderChoices
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event


class Profile(models.Model, AggregateBase):
  profile_uid = models.CharField(max_length=100, unique=True)
  profile_external_id = models.CharField(max_length=2400)
  profile_attrs = JSONField()
  provider_type = models.PositiveSmallIntegerField(choices=ProviderChoices)
  prospect = models.ForeignKey('prospect.Prospect', related_name="profiles")
  system_created_date = models.DateTimeField()


  class Meta:
    unique_together = ("profile_external_id", "provider_type")


  @classmethod
  def _from_provider_info_and_profile_attrs(cls, prospect_id, profile_external_id, provider_type, profile_attrs):
    ret_val = cls()

    if not prospect_id:
      raise TypeError("prospect id is required")

    if not profile_external_id:
      raise TypeError("external id is required")

    ret_val._raise_event(
      created,
      profile_uid=str(uuid.uuid1()),
      prospect_id=prospect_id,
      profile_external_id=profile_external_id,
      profile_attrs=profile_attrs,
      provider_type=provider_type,
      system_created_date=timezone.now()
    )

    return ret_val


  def _handle_created_event(self, **kwargs):
    self.profile_uid = kwargs['profile_uid']
    self.prospect_id = kwargs['prospect_id']
    self.profile_external_id = kwargs['profile_external_id']
    self.profile_attrs = kwargs['profile_attrs']
    self.provider_type = kwargs['provider_type']
    self.system_created_date = kwargs['system_created_date']

  def __str__(self):
    return 'Profile #' + str(self.pk) + ': ' + self.profile_external_id

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      self.send_events()
    else:
      from src.aggregates.profile.services import profile_service

      profile_service.save_or_update(self)
