import logging
from src.apps.engagement_discovery.providers.reddit import reddit_engagement_discovery_provider
from src.apps.engagement_discovery.providers.twitter import twitter_engagement_discovery_provider

logger = logging.getLogger(__name__)


def discover_engagement_opportunities():
  logger.debug('run providers begin')
  twitter_engagement_discovery_provider.discover_engagement_opportunities()
  reddit_engagement_discovery_provider.discover_engagement_opportunities()
  logger.debug('run providers end')
