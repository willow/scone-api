from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.recommendation.recommendation_builder import RecommendationBuilder
from src.aggregates.engagement_assignment.recommendation.recommendation_data_providers\
  .linkedin_recommendation_provider import \
  LinkedinRecommendationDataProvider
from src.aggregates.engagement_assignment.recommendation.recommendation_data_providers\
  .reddit_recommendation_data_provider import \
  RedditRecommendationDataProvider
from src.aggregates.engagement_assignment.recommendation.recommendation_data_providers\
  .twitter_recommendation_data_provider import \
  TwitterRecommendationDataProvider
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service
from src.apps.engagement_discovery.enums import ProviderEnum


def recommend_action(client, assignment_attrs):
  
  ret_val = []
  
  if constants.ASSIGNED_EO_IDS in assignment_attrs:
    assigned_entity_type = constants.ASSIGNED_EO_IDS
    entity_type = constants.EO
  elif constants.ASSIGNED_PROFILE_IDS in assignment_attrs:
    assigned_entity_type = constants.ASSIGNED_PROFILE_IDS
    entity_type = constants.PROFILE
  else:
    raise ValueError("Invalid assignment attrs")

  for assigned_entity_id in assignment_attrs[assigned_entity_type]:
    
    data_provider = _get_data_provider(assigned_entity_id, assigned_entity_type)
    
    recommendation_data = data_provider.provide_recommendation_data(client, assigned_entity_id, assigned_entity_type)
    
    builder = RecommendationBuilder(recommendation_data)
    
    recommendation = builder.build_recommended_action()

    ret_val.append({'recommendation': recommendation, 'entity_type': entity_type,
                    'id': assigned_entity_id})
    
  return ret_val

def _get_data_provider(assigned_entity_id, assigned_entity_type):
  
  if assigned_entity_type == constants.ASSIGNED_EO_IDS:
    
    engagement_opportunity = engagement_opportunity_service.get_engagement_opportunity(assigned_entity_id)
    
    if engagement_opportunity.provider_type == ProviderEnum.twitter:
      return TwitterRecommendationDataProvider()
    elif engagement_opportunity.provider_type == ProviderEnum.reddit:
      return RedditRecommendationDataProvider()
    
  elif assigned_entity_type == constants.ASSIGNED_PROFILE_IDS:
    
    profile = profile_service.get_profile(assigned_entity_id)
    
    if profile.provider_type == ProviderEnum.linkedin:
      return LinkedinRecommendationDataProvider()
    
  raise ValueError("Invalid provider type")
