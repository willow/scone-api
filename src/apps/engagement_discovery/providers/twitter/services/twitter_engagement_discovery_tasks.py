from src.aggregates.topic.enums import TopicCategoryEnum
from src.aggregates.topic.services import topic_service
from src.apps.engagement_discovery.providers.twitter.services.twitter_engagement_discovery_service import (
  discover_engagement_opportunities_from_twitter_subtopic
)

from celery import shared_task


@shared_task
def discover_engagement_opportunities_from_twitter_subtopics_task(kwargs=None):
  if not kwargs: kwargs = {}

  topics_to_run = topic_service.get_active_topics()

  for topic in topics_to_run:
    for subtopic in topic.subtopics.all():
      if subtopic.category_type == TopicCategoryEnum.twitter_search:
        discover_engagement_opportunities_from_twitter_subtopic_task.delay(subtopic.id, kwargs)


@shared_task
def discover_engagement_opportunities_from_twitter_subtopic_task(subtopic_id, kwargs=None):
  if not kwargs: kwargs = {}
  subtopic = topic_service.get_subtopic(subtopic_id)
  return discover_engagement_opportunities_from_twitter_subtopic(subtopic, **kwargs)


@shared_task
def discover_engagement_opportunities_from_user_task(profile_id, kwargs=None):
  if not kwargs: kwargs = {}
  kwargs['profile_id'] = profile_id
  discover_engagement_opportunities_from_twitter_subtopics_task.delay(kwargs)
