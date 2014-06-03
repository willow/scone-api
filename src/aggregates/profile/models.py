from django.db import models, transaction
from jsonfield import JSONField
import reversion
import uuid

from src.aggregates.profile.signals import created
from src.apps.engagement_discovery.enums import ProviderChoices
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import RevisionEvent
from src.libs.django_utils.serialization.flexible_json_serializer import JSONSerializer


class Profile(models.Model, AggregateBase):
  profile_uid = models.CharField(max_length=100, unique=True)
  profile_external_id = models.CharField(max_length=2400)
  profile_attrs = JSONField(blank=True, null=True)
  provider_type = models.PositiveSmallIntegerField(choices=ProviderChoices)


  class Meta:
    unique_together = ("profile_external_id", "provider_type")


  @classmethod
  def _from_provider_info_and_profile_attrs(cls, profile_external_id, provider_type, profile_attrs):
    ret_val = cls()

    if not profile_external_id:
      raise TypeError("external id is required")

    ret_val._raise_event(
      created, sender=Profile, instance=ret_val,
      profile_uid=str(uuid.uuid1()),
      profile_external_id=profile_external_id,
      profile_attrs=profile_attrs,
      provider_type=provider_type,
    )

    return ret_val


  def _handle_created_event(self, **kwargs):
    self.profile_uid = kwargs['profile_uid']
    self.profile_external_id = kwargs['profile_external_id']
    self.profile_attrs = kwargs['profile_attrs']
    self.provider_type = kwargs['provider_type']

  def __str__(self):
    return 'Profile #' + str(self.pk) + ': ' + self.profile_external_id

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        with reversion.create_revision():
          super().save(*args, **kwargs)

          serializer = JSONSerializer()

          for event in self._uncommitted_events:
            # we don't need to store the instance because it's not really part of the parameters
            #and django-reversion will keep a snapshop
            kwargs_to_save = {k: v for k, v in event.kwargs.items() if k != 'instance'}

            data = serializer.serialize(kwargs_to_save)

            reversion.add_meta(RevisionEvent, name=event.event_fq_name, version=event.version, data=data)

      self.send_events()
    else:
      from src.aggregates.profile.services import profile_service

      profile_service.save_or_update(self)
