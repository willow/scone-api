from src.aggregates.topic.services import topic_service
from src.apps.engagement_discovery.providers.reddit.services.reddit_engagement_discovery_service import \
  discover_engagement_opportunities_from_subreddit

from celery import shared_task


@shared_task
def discover_engagement_opportunities_from_subreddits_task(subtopic_id):
  subtopic = topic_service.get_subtopic(subtopic_id)
  return discover_engagement_opportunities_from_subreddit(subtopic)
