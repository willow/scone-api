from src.aggregates.topic.enums import TopicCategoryEnum
from src.aggregates.topic.services import topic_service
from src.apps.engagement_discovery.providers.reddit.services.reddit_engagement_discovery_service import \
  discover_engagement_opportunities_from_subreddit

from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def discover_engagement_opportunities_from_subreddits_task():
  topics_to_run = topic_service.get_active_topics()

  for topic in topics_to_run:
    for subtopic in topic.subtopics.all():
      if subtopic.category_type == TopicCategoryEnum.subreddit:
        discover_engagement_opportunities_from_subreddit_task.delay(subtopic.id)


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def discover_engagement_opportunities_from_subreddit_task(self, subtopic_id):
  subtopic = topic_service.get_subtopic(subtopic_id)
  try:
    ret_val = discover_engagement_opportunities_from_subreddit(subtopic)
    return ret_val
  except IOError as e:
    self.retry(exc=e)
