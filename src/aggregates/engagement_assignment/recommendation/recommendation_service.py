from src.aggregates.engagement_assignment.recommendation.recommendation_builder import RecommendationBuilder
from src.aggregates.engagement_assignment.recommendation.recommendation_data_providers\
  .reddit_recommendation_data_provider import \
  RedditRecommendationDataProvider
from src.aggregates.engagement_assignment.recommendation.recommendation_data_providers\
  .twitter_recommendation_data_provider import \
  TwitterRecommendationDataProvider
from src.apps.engagement_discovery.enums import ProviderEnum


def recommend_action(client, engagement_opportunity):
  data_provider = _get_data_provider(engagement_opportunity)
  recommendation_data = data_provider.provide_recommendation_data(client, engagement_opportunity)
  
  builder = RecommendationBuilder(recommendation_data)
  return builder.build_recommended_action()

def _get_data_provider(engagement_opportunity):
  # hardcoded to twitter for onw
  if engagement_opportunity.provider_type == ProviderEnum.twitter:
    return TwitterRecommendationDataProvider()
  elif engagement_opportunity.provider_type == ProviderEnum.reddit:
    return RedditRecommendationDataProvider()
