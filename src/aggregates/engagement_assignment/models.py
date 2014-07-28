from django.db import models, transaction
from django.utils import timezone
from jsonfield import JSONField
from src.libs.common_domain.models import Event
import uuid

from src.aggregates.engagement_assignment.calculation import calculate_score_service
from src.aggregates.engagement_assignment.recommendation import recommendation_service
from src.aggregates.engagement_assignment.signals import created, delivered
from src.libs.common_domain.aggregate_base import AggregateBase


class EngagementAssignment(models.Model, AggregateBase):
  engagement_assignment_uid = models.CharField(max_length=2400, db_index=True)
  client = models.ForeignKey('client.Client', related_name="assignments")
  assignment_attrs = JSONField()
  score = models.DecimalField(max_digits=19, decimal_places=7, db_index=True)
  score_attrs = JSONField()
  system_created_date = models.DateTimeField()

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._recommendation = None


  @classmethod
  def _from_client_and_engagement_opportunity(cls, client, assignment_attrs,
                                              _calc_score_service=calculate_score_service,
                                              _recommendation_service=recommendation_service):
    ret_val = cls()

    if not client:
      raise TypeError("client is required")

    if not isinstance(assignment_attrs, dict):
      raise TypeError("assignment_attrs must be a dict")

    for k, v in assignment_attrs.items():
      if not isinstance(v, (list, tuple)):
        raise TypeError("Each value must be an iterable")

    score, score_attrs = _calc_score_service.calculate_engagement_assignment_score(client, assignment_attrs)

    recommended_action = _recommendation_service.recommend_action(client, assignment_attrs)

    client_id = client.id

    ret_val._raise_event(
      created, engagement_assignment_uid=str(uuid.uuid1()),
      client_id=client_id, assignment_attrs=assignment_attrs, score=score, score_attrs=score_attrs,
      recommended_action=recommended_action, system_created_date=timezone.now()
    )

    return ret_val

  def deliver(self):
    self._raise_event(
      delivered, engagement_assignment_uid=self.engagement_assignment_uid, system_created_date=timezone.now()
    )

  def _handle_created_event(self, **kwargs):
    self.engagement_assignment_uid = kwargs['engagement_assignment_uid']
    self.client_id = kwargs['client_id']
    self.assignment_attrs = kwargs['assignment_attrs']
    self.score = kwargs['score']
    self.score_attrs = kwargs['score_attrs']
    self._recommendation = Recommendation(recommended_action=kwargs['recommended_action'])
    self.system_created_date = kwargs['system_created_date']

  def _handle_delivered_event(self, **kwargs):
    pass

  def __str__(self):
    return 'Engagement Assignment #' + str(self.pk) + ': ' + str(self.score)

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)

        if self._recommendation:
          self.recommendation = self._recommendation
          self.recommendation.save()

        for event in self._uncommitted_events:
          Event.objects.create(name=event.event_fq_name, version=event.version, data=event.kwargs)

      self.send_events()
    else:
      from src.aggregates.engagement_assignment.services import engagement_assignment_service

      engagement_assignment_service.save_or_update(self)


class Recommendation(models.Model):
  engagement_assignment = models.OneToOneField(EngagementAssignment, primary_key=True, related_name='recommendation')
  recommended_action = models.TextField()
