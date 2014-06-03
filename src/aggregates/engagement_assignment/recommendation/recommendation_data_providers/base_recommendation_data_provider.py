from abc import ABC
from src.aggregates.engagement_assignment import constants


class BaseRecommendationDataProvider(ABC):
  def provide_recommendation_data(self, client, engagement_opportunity):
    ret_val = {}

    eo_attrs = engagement_opportunity.engagement_opportunity_attrs
    ret_val[constants.PROVIDER_TYPE] = engagement_opportunity.provider_type

    return ret_val
