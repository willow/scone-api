from django.db import models, transaction
import reversion
import uuid
from src.aggregates.topic.enums import TopicCategoryChoices

from src.aggregates.topic.signals import created, added_subtopic
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import RevisionEvent
from src.libs.django_utils.serialization.flexible_json_serializer import JSONSerializer
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

  @classmethod
  def _from_attrs(cls, topic_name, _slugify_utils=slugify_utils, _iter_utils=iter_utils):
    ret_val = cls()

    if not topic_name:
      raise TypeError("topic name is required")

    system_name = _slugify_utils.create_slug(topic_name)
    snowball_stem = _iter_utils.stemmify_string(topic_name)
    
    ret_val._raise_event(
      created, sender=Topic, instance=ret_val,
      topic_uid=str(uuid.uuid1()),
      system_name=system_name,
      topic_name=topic_name,
      snowball_stem=snowball_stem
    )

    return ret_val

  def associate_subtopic_with_topic(self, subtopic_name, category_type):
    self._raise_event(
      added_subtopic, sender=Topic, instance=self,
      subtopic_uid=str(uuid.uuid1()),
      subtopic_name=subtopic_name,
      category_type=category_type,
    )

  def _handle_created_event(self, **kwargs):
    self.topic_uid = kwargs['topic_uid']
    self.system_name = kwargs['system_name']
    self.topic_name = kwargs['topic_name']
    self.snowball_stem = kwargs['snowball_stem']

  def _handle_added_subtopic_event(self, **kwargs):
    subtopic_uid = kwargs['subtopic_uid']
    subtopic_name = kwargs['subtopic_name']
    category_type = kwargs['category_type']

    self._subtopics_list.append(Subtopic(
      subtopic_uid=subtopic_uid,
      subtopic_name=subtopic_name,
      category_type=category_type
    ))

  def __str__(self):
    return 'Topic #' + str(self.pk) + ': ' + self.topic_name

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        with reversion.create_revision():
          super().save(*args, **kwargs)

          for subtopic in self._subtopics_list:
            self.subtopics.add(subtopic)

          serializer = JSONSerializer()

          for event in self._uncommitted_events:
            # we don't need to store the instance because it's not really part of the parameters
            # and django-reversion will keep a snapshop
            kwargs_to_save = {k: v for k, v in event.kwargs.items() if k != 'instance'}

            data = serializer.serialize(kwargs_to_save)

            reversion.add_meta(RevisionEvent, name=event.event_fq_name, version=event.version, data=data)

      self.send_events()
    else:
      from src.aggregates.topic.services import topic_service

      topic_service.save_or_update(self)


class Subtopic(models.Model):
  subtopic_uid = models.CharField(max_length=100, unique=True)
  subtopic_name = models.CharField(max_length=2400)
  topic = models.ForeignKey(Topic, related_name='subtopics')
  category_type = models.PositiveSmallIntegerField(choices=TopicCategoryChoices)

  def __str__(self):
    return 'Subtopic #' + str(self.pk) + ': ' + self.subtopic_name
