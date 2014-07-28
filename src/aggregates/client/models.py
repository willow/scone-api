from django.db import models, transaction
from src.aggregates.client.signals import added_ta_topic, created, deleted, removed_ta_topic, disabled, enabled
import uuid
from src.aggregates.client.enums import ClientTypeChoices

from src.aggregates.topic.models import Topic
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event


class Client(models.Model, AggregateBase):
  client_uid = models.CharField(max_length=100, unique=True)
  client_name = models.CharField(max_length=2400)
  client_type = models.PositiveSmallIntegerField(choices=ClientTypeChoices)
  enabled = models.BooleanField(default=None)  # default none prevents 1_6.W002

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._ta_topics_list = []
    self._ta_topics_delete_list = []

  @classmethod
  def _from_attrs(cls, client_name, client_type):
    ret_val = cls()

    if not client_name:
      raise TypeError("client name is required")

    if not client_type:
      raise TypeError("client type is required")

    ret_val._raise_event(
      created,
      client_uid=str(uuid.uuid1()),
      client_name=client_name,
      client_type=client_type,
    )

    return ret_val


  def add_ta_topic(self, topic_type_id):
    if not topic_type_id:
      raise TypeError("topic_type_id is required")

    self._raise_event(
      added_ta_topic, client_uid=self.client_uid,
      ta_topic_uid=str(uuid.uuid1()), topic_type_id=topic_type_id
    )

  def remove_ta_topic(self, ta_topic):
    self._raise_event(
      removed_ta_topic,
      client_uid=self.client_uid,
      ta_topic_uid=ta_topic.ta_topic_uid
    )

  def disable(self):
    self._raise_event(disabled, client_uid=self.client_uid)

  def _handle_disabled_event(self, **kwargs):
    self.enabled = False

  def enable(self):
    self._raise_event(enabled, client_uid=self.client_uid)

  def _handle_enabled_event(self, **kwargs):
    self.enabled = True

  def _handle_created_event(self, **kwargs):
    self.client_uid = kwargs['client_uid']
    self.client_name = kwargs['client_name']
    self.client_type = kwargs['client_type']
    self.enabled = True

  def _handle_added_ta_topic_event(self, **kwargs):
    ta_topic_uid = kwargs['ta_topic_uid']
    topic_type_id = kwargs['topic_type_id']

    self._ta_topics_list.append(TATopic(ta_topic_uid=ta_topic_uid, topic_type_id=topic_type_id))

  def _handle_removed_ta_topic_event(self, **kwargs):
    ta_topic_uid = kwargs['ta_topic_uid']
    ta_topic = self.ta_topics.get(ta_topic_uid=ta_topic_uid)

    self._ta_topics_delete_list.append(ta_topic)

  def _handle_deleted_event(self, **kwargs):
    pass

  def __str__(self):
    return 'Client #' + str(self.pk) + ': ' + self.client_name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for ta in self._ta_topics_list:
          # add actually does a save internally, hitting the db
          self.ta_topics.add(ta)

        for ta in self._ta_topics_delete_list:
          ta.delete()

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      self.send_events()
    else:
      from src.aggregates.client.services import client_service

      client_service.save_or_update(self)


  def delete(self, internal=False, using=None):
    if internal:
      with transaction.atomic():

        self._raise_event(
          deleted,
          client_uid=self.client_uid,
        )

        super().delete(using)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      self.send_events()
    else:
      from src.aggregates.client.services import client_service

      client_service.delete_client(self)


class TATopic(models.Model):
  ta_topic_uid = models.CharField(max_length=100, unique=True)
  client = models.ForeignKey(Client, related_name='ta_topics')
  topic_type = models.ForeignKey(Topic, related_name='client_ta_topics')

  class Meta:
    unique_together = ("client", "topic_type")
