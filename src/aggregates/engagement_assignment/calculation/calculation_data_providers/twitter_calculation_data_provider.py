from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.calculation_data_providers.base_calculation_data_provider import \
  BaseCalculationDataProvider


class TwitterCalculationDataProvider(BaseCalculationDataProvider):
  def provide_calculation_data(self, client, engagement_opportunity):
    ret_val = super().provide_calculation_data(client, engagement_opportunity)

    eo_attrs = engagement_opportunity.engagement_opportunity_attrs
    profile_attrs = engagement_opportunity.profile.profile_attrs

    ret_val[constants.BIO] = profile_attrs.get(constants.BIO)
    ret_val[constants.BIO_TA_TOPIC_SCORE_MULTIPLIER] = 3

    ret_val[constants.NAME] = profile_attrs.get(constants.NAME)
    ret_val[constants.PROFILE_WEBSITES] = profile_attrs.get(constants.WEBSITES)
    ret_val[constants.LOCATION] = profile_attrs.get(constants.LOCATION)
    ret_val[constants.FOLLOWERS_COUNT] = profile_attrs.get(constants.FOLLOWERS_COUNT, 0)
    ret_val[constants.RECENT_POSTS] = profile_attrs.get(constants.RECENT_TWEETS)
    ret_val[constants.RECENT_POST_TA_TOPIC_SCORE_MULTIPLIER] = 1

    ret_val[constants.TEXT] = eo_attrs.get(constants.TEXT)
    ret_val[constants.TEXT_HTML] = eo_attrs.get(constants.TEXT_HTML)
    ret_val[constants.EO_WEBSITES] = eo_attrs.get(constants.WEBSITES)
    ret_val[constants.EO_WEBSITE_TA_TOPIC_SCORE_MULTIPLIER] = 1

    ret_val[constants.CREATED_DATE] = engagement_opportunity.created_date

    ret_val[constants.SUBMISSION_OWNER] = True
    ret_val[constants.SUBMISSION_OWNER_SCORE_MULTIPLIER] = 0

    return ret_val
