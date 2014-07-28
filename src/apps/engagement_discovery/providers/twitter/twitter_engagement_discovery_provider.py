from src.apps.engagement_discovery.providers.twitter.services.twitter_engagement_discovery_tasks import \
  discover_engagement_opportunities_from_twitter_subtopics_task


def discover_engagement_opportunities():
  # Find all keywords that are ready to be ran
  # Iterate through keywords and kick off celery task to do twitter searches
  # Hand off to twitter service to analyze tweets and filter
  # Hand off remaining tweets to core library to analyze and filter

  discover_engagement_opportunities_from_twitter_subtopics_task.delay()
