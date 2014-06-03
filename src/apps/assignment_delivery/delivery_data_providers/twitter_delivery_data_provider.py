from src.apps.assignment_delivery import constants
from src.apps.assignment_delivery.delivery_data_providers.base_delivery_data_provider import BaseDeliveryDataProvider


class TwitterDeliveryDataProvider(BaseDeliveryDataProvider):
  def provide_delivery_data(self, engagement_assignment):
    ret_val = super().provide_delivery_data(engagement_assignment)

    engagement_opportunity = engagement_assignment.engagement_opportunity

    eo_attrs = engagement_opportunity.engagement_opportunity_attrs
    profile_attrs = engagement_opportunity.profile.profile_attrs

    ret_val[constants.USERNAME] = profile_attrs[constants.PROFILE_URL]
    ret_val[constants.NAME] = profile_attrs[constants.NAME]
    ret_val[constants.FOLLOWERS_COUNT] = profile_attrs[constants.FOLLOWERS_COUNT]
    ret_val[constants.FOLLOWING_COUNT] = profile_attrs[constants.FOLLOWING_COUNT]
    ret_val[constants.ENGAGEMENT_OPPORTUNITY_URL] = eo_attrs[constants.URL]
    ret_val[constants.RECOMMENDATION] = engagement_assignment.recommendation.recommended_action
    ret_val[constants.BIO] = profile_attrs.get(constants.BIO)

    return ret_val


