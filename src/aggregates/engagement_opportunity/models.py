from django.db import models, transaction
from django.utils import timezone
from jsonfield import JSONField
import uuid

from src.aggregates.engagement_opportunity.signals import created, added_topic
from src.aggregates.topic.models import Topic
from src.apps.engagement_discovery.enums import ProviderChoices, ProviderEnum, ProviderActionChoices
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event


class EngagementOpportunity(models.Model, AggregateBase):
  engagement_opportunity_uid = models.CharField(max_length=100, unique=True)
  engagement_opportunity_external_id = models.CharField(max_length=2400, db_index=True)
  engagement_opportunity_attrs = JSONField(blank=True, null=True)
  profile = models.ForeignKey('profile.Profile', related_name='engagement_opportunities')
  provider_type = models.PositiveSmallIntegerField(choices=ProviderChoices)
  provider_action_type = models.PositiveSmallIntegerField(choices=ProviderActionChoices)
  created_date = models.DateTimeField()
  system_created_date = models.DateTimeField()

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._topics_list = []

  class Meta:
    unique_together = ("engagement_opportunity_external_id", "provider_type")

  @classmethod
  def _from_engagement_discovery(cls, profile_id, engagement_opportunity_discovery_object):
    ret_val = cls()

    if not profile_id:
      raise TypeError("profile_id is required")

    if not engagement_opportunity_discovery_object:
      raise TypeError("eo is required")

    ret_val._raise_event(
      created,
      engagement_opportunity_uid=str(uuid.uuid1()),
      engagement_opportunity_external_id=engagement_opportunity_discovery_object.engagement_opportunity_external_id,
      engagement_opportunity_attrs=engagement_opportunity_discovery_object.engagement_opportunity_attrs,
      profile_id=profile_id,
      provider_type=engagement_opportunity_discovery_object.provider_type,
      provider_action_type=engagement_opportunity_discovery_object.provider_action_type,
      created_date=engagement_opportunity_discovery_object.created_date,
      system_created_date=timezone.now()
    )

    return ret_val

  def associate_with_topic(self, topic):
    self._raise_event(
      added_topic, engagement_opportunity_uid=self.engagement_opportunity_uid,
      engagement_opportunity_topic_uid=str(uuid.uuid1()),
      topic_type_id=topic.id
    )


  def _handle_created_event(self, **kwargs):
    self.engagement_opportunity_uid = kwargs['engagement_opportunity_uid']
    self.engagement_opportunity_external_id = kwargs['engagement_opportunity_external_id']
    self.engagement_opportunity_attrs = kwargs['engagement_opportunity_attrs']
    self.profile_id = kwargs['profile_id']
    self.provider_type = kwargs['provider_type']
    self.provider_action_type = kwargs['provider_action_type']
    self.created_date = kwargs['created_date']
    self.system_created_date = kwargs['system_created_date']

  def _handle_added_topic_event(self, **kwargs):
    engagement_opportunity_topic_uid = kwargs['engagement_opportunity_topic_uid']
    topic_type_id = kwargs['topic_type_id']

    self._topics_list.append(EngagementOpportunityTopic(
      engagement_opportunity_topic_uid=engagement_opportunity_topic_uid, topic_type_id=topic_type_id)
    )

  def __str__(self):
    return 'Engagement Opportunity #' + str(self.pk) + ': ' + ProviderEnum(self.provider_type).name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for topic in self._topics_list:
          self.topics.add(topic)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      self.send_events()
    else:
      from src.aggregates.engagement_opportunity.services import engagement_opportunity_service

      engagement_opportunity_service.save_or_update(self)


class EngagementOpportunityTopic(models.Model):
  engagement_opportunity_topic_uid = models.CharField(max_length=100, unique=True)
  engagement_opportunity = models.ForeignKey(EngagementOpportunity, related_name='topics')
  topic_type = models.ForeignKey(Topic, related_name='engagement_opportunity_topics')

  class Meta:
    unique_together = ("engagement_opportunity", "topic_type")
