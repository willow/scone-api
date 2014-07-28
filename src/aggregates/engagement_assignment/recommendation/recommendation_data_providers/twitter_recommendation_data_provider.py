from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.recommendation.recommendation_data_providers \
  .base_recommendation_data_provider import \
  BaseRecommendationDataProvider
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service


class TwitterRecommendationDataProvider(BaseRecommendationDataProvider):
  def provide_recommendation_data(self, client, engagement_opportunity_id, assigned_entity_type):
      
    ret_val = super().provide_recommendation_data(client, engagement_opportunity_id, assigned_entity_type)
    
    engagement_opportunity = engagement_opportunity_service.get_engagement_opportunity(engagement_opportunity_id)

    eo_attrs = engagement_opportunity.engagement_opportunity_attrs
    profile_attrs = engagement_opportunity.profile.profile_attrs

    ret_val[constants.NAME] = profile_attrs[constants.NAME]
    ret_val[constants.TEXT] = eo_attrs[constants.TEXT]

    ret_val[constants.CONTAINS_LINK] = True if 'http' in eo_attrs[constants.TEXT] else False

    return ret_val
