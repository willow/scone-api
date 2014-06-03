import collections
from django.db import models, transaction
from django.utils import timezone
from jsonfield import JSONField
import reversion
import uuid

from src.aggregates.engagement_assignment.calculation import calculate_score_service
from src.aggregates.engagement_assignment.recommendation import recommendation_service
from src.aggregates.engagement_assignment.signals import created
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.common_domain.models import RevisionEvent
from src.libs.django_utils.serialization.flexible_json_serializer import JSONSerializer


class EngagementAssignment(models.Model, AggregateBase):
  engagement_assignment_uid = models.CharField(max_length=2400, db_index=True)
  client = models.ForeignKey('client.Client', related_name="assignments")
  engagement_opportunity = models.ForeignKey('engagement_opportunity.EngagementOpportunity', related_name="assignments")
  score = models.DecimalField(max_digits=19, decimal_places=7, db_index=True)
  score_attrs = JSONField()
  system_created_date = models.DateTimeField()

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._recommendation = None


  class Meta:
    unique_together = ("client", "engagement_opportunity")

  @classmethod
  def _from_client_and_engagement_opportunity(cls, client, engagement_opportunity,
                                              _calc_score_service=calculate_score_service,
                                              _recommendation_service=recommendation_service):
    ret_val = cls()

    if not client:
      raise TypeError("client is required")

    if not engagement_opportunity:
      raise TypeError("eo is required")

    score, score_attrs = _calc_score_service.calculate_engagement_assignment_score(client, engagement_opportunity)

    recommended_action = _recommendation_service.recommend_action(client, engagement_opportunity)

    client_id = client.id
    engagement_opportunity_id = engagement_opportunity.id

    ret_val._raise_event(
      created, sender=EngagementAssignment, instance=ret_val, engagement_assignment_uid=str(uuid.uuid1()),
      client_id=client_id, engagement_opportunity_id=engagement_opportunity_id, score=score, score_attrs=score_attrs,
      recommended_action=recommended_action, system_created_date=timezone.now()
    )

    return ret_val

  def _handle_created_event(self, **kwargs):
    self.engagement_assignment_uid = kwargs['engagement_assignment_uid']
    self.client_id = kwargs['client_id']
    self.engagement_opportunity_id = kwargs['engagement_opportunity_id']
    self.score = kwargs['score']
    self.score_attrs = kwargs['score_attrs']
    self._recommendation = Recommendation(recommended_action=kwargs['recommended_action'])
    self.system_created_date = kwargs['system_created_date']

  def __str__(self):
    return 'Engagement Assignment #' + str(self.pk) + ': ' + str(self.score)

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        with reversion.create_revision():
          super().save(*args, **kwargs)

          if self._recommendation:
            self.recommendation = self._recommendation
            self.recommendation.save()

          serializer = JSONSerializer()

          for event in self._uncommitted_events:
            # we don't need to store the instance because it's not really part of the parameters
            # and django-reversion will keep a snapshop
            kwargs_to_save = {k: v for k, v in event.kwargs.items() if k != 'instance'}

            data = serializer.serialize(kwargs_to_save)

            reversion.add_meta(RevisionEvent, name=event.event_fq_name, version=event.version, data=data)

      self.send_events()
    else:
      from src.aggregates.engagement_assignment.services import engagement_assignment_service

      engagement_assignment_service.save_or_update(self)


class Recommendation(models.Model):
  engagement_assignment = models.OneToOneField(EngagementAssignment, primary_key=True, related_name='recommendation')
  recommended_action = models.TextField()
