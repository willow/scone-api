from abc import ABC
from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service


class BaseRecommendationDataProvider(ABC):
  def provide_recommendation_data(self, client, assigned_entity_id, assigned_entity_type):
    ret_val = {}
    
    if assigned_entity_type == constants.ASSIGNED_EO_UIDS:
      
      engagement_opportunity = engagement_opportunity_service.get_engagement_opportunity(assigned_entity_id)
      assignment_attrs = engagement_opportunity.engagement_opportunity_attrs
      ret_val[constants.PROVIDER_TYPE] = engagement_opportunity.provider_type
      
    elif assigned_entity_type == constants.ASSIGNED_PROFILE_UIDS:
      
      profile = profile_service.get_profile(assigned_entity_id)
      assignemnt_attrs = profile.profile_attrs
      ret_val[constants.PROVIDER_TYPE] = profile.provider_type
      
    else:
      
      ValueError("Invalid provider type")
      
    return ret_val
