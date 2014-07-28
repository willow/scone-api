from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.recommendation.recommendation_data_providers \
  .base_recommendation_data_provider import \
  BaseRecommendationDataProvider
from src.aggregates.profile.services import profile_service


class LinkedinRecommendationDataProvider(BaseRecommendationDataProvider):
  def provide_recommendation_data(self, client, profile_id, assigned_entity_type):
    ret_val = super().provide_recommendation_data(client, profile_id, assigned_entity_type)

    profile = profile_service.get_profile(profile_id)

    profile_attrs = profile.profile_attrs

    # linkedin users sometimes mark their data as private - provide defaults
    ret_val[constants.NAME] = profile_attrs.get(constants.NAME, str(profile_id))
    ret_val[constants.TEXT] = profile_attrs.get(constants.TEXT, str(profile_id))

    ret_val[constants.CONTAINS_LINK] = True if 'http' in ret_val[constants.TEXT] else False

    return ret_val
