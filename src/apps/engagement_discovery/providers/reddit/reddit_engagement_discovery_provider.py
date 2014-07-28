from src.apps.engagement_discovery.providers.reddit.services.reddit_engagement_discovery_tasks import \
  discover_engagement_opportunities_from_subreddits_task


def discover_engagement_opportunities():
  # Find all keywords that are ready to be ran
  # Iterate through keywords and kick off celery task to do reddit searches
  # Hand off to reddit service to analyze tweets and filter
  # Hand off remaining items to core library to analyze and filter
  discover_engagement_opportunities_from_subreddits_task.delay()
