from django.db import models, transaction
from jsonfield import JSONField
import uuid
from src.aggregates.topic.enums import TopicCategoryChoices, TopicCategoryEnum

from src.aggregates.topic.signals import created, added_subtopic, deleted, removed_subtopic, updated_attrs
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import Event
from src.libs.python_utils.collections import iter_utils
from src.libs.text_utils.slugify import slugify_utils


class Topic(models.Model, AggregateBase):
  topic_uid = models.CharField(max_length=100, unique=True)
  system_name = models.CharField(max_length=2004, unique=True)
  topic_name = models.CharField(max_length=2400)
  snowball_stem = models.CharField(max_length=2400)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._subtopics_list = []
    self._subtopics_delete_list = []

  @classmethod
  def _from_attrs(cls, topic_name, _slugify_utils=slugify_utils, _iter_utils=iter_utils):
    ret_val = cls()

    if not topic_name:
      raise TypeError("topic name is required")

    system_name = _slugify_utils.create_slug(topic_name)
    snowball_stem = _iter_utils.stemmify_string(topic_name)

    ret_val._raise_event(
      created,
      topic_uid=str(uuid.uuid1()),
      system_name=system_name,
      topic_name=topic_name,
      snowball_stem=snowball_stem
    )

    return ret_val

  def associate_subtopic_with_topic(self, subtopic_name, category_type, subtopic_attrs, _iter_utils=iter_utils):
    if category_type == TopicCategoryEnum.keywords:
      snowball_stem = _iter_utils.stemmify_string(subtopic_name)
      subtopic_attrs['snowball_stem'] = snowball_stem

    self._raise_event(
      added_subtopic, topic_uid=self.topic_uid,
      subtopic_uid=str(uuid.uuid1()),
      subtopic_name=subtopic_name,
      category_type=category_type,
      subtopic_attrs=subtopic_attrs
    )

  def remove_subtopic(self, subtopic):
    self._raise_event(
      removed_subtopic, topic_uid=self.topic_uid,
      subtopic_uid=subtopic.subtopic_uid,
    )

  # todo these deps should be injected in the ctr, not each instance method. Also, change iter_utils for stemmify str
  def update_attrs(self, topic_attrs, _slugify_utils=slugify_utils, _iter_utils=iter_utils):
    topic_name = topic_attrs.get('topic_name')

    if topic_name:
      topic_attrs['system_name'] = _slugify_utils.create_slug(topic_name)
      topic_attrs['snowball_stem'] = _iter_utils.stemmify_string(topic_name)

    self._raise_event(
      updated_attrs, topic_uid=self.topic_uid,
      topic_attrs=topic_attrs
    )

  def _handle_created_event(self, **kwargs):
    self.topic_uid = kwargs['topic_uid']
    self.system_name = kwargs['system_name']
    self.topic_name = kwargs['topic_name']
    self.snowball_stem = kwargs['snowball_stem']

  def _handle_deleted_event(self, **kwargs):
    pass

  def _handle_added_subtopic_event(self, **kwargs):
    subtopic_uid = kwargs['subtopic_uid']
    subtopic_name = kwargs['subtopic_name']
    category_type = kwargs['category_type']
    subtopic_attrs = kwargs['subtopic_attrs']

    self._subtopics_list.append(Subtopic(
      subtopic_uid=subtopic_uid,
      subtopic_name=subtopic_name,
      category_type=category_type,
      subtopic_attrs=subtopic_attrs
    ))

  def _handle_removed_subtopic_event(self, **kwargs):
    subtopic_uid = kwargs['subtopic_uid']
    sub = self.subtopics.get(subtopic_uid=subtopic_uid)
    self._subtopics_delete_list.append(sub)

  def _handle_updated_attrs_event(self, **kwargs):
    topic_attrs = kwargs['topic_attrs']

    for k, v in topic_attrs.items():
      setattr(self, k, v)

  def __str__(self):
    return 'Topic #' + str(self.pk) + ': ' + self.topic_name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        for subtopic in self._subtopics_list:
          self.subtopics.add(subtopic)

        for subtopic in self._subtopics_delete_list:
          subtopic.delete()

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      self.send_events()
    else:
      from src.aggregates.topic.services import topic_service

      topic_service.save_or_update(self)


  def delete(self, internal=False, using=None):
    if internal:
      with transaction.atomic():

        self._raise_event(
          deleted,
          topic_uid=self.topic_uid,
        )

        super().delete(using)

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      self.send_events()
    else:
      from src.aggregates.topic.services import topic_service

      topic_service.delete_topic(self)


class Subtopic(models.Model):
  subtopic_uid = models.CharField(max_length=100, unique=True)
  subtopic_name = models.CharField(max_length=2400)
  topic = models.ForeignKey(Topic, related_name='subtopics')
  category_type = models.PositiveSmallIntegerField(choices=TopicCategoryChoices)
  subtopic_attrs = JSONField(blank=True)


  def __str__(self):
    return 'Subtopic #' + str(self.pk) + ': ' + self.subtopic_name
