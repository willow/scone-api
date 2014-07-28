from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.calculation_data_providers.base_calculation_data_provider import \
  BaseCalculationDataProvider
from src.aggregates.engagement_opportunity.models import EngagementOpportunity


class TwitterCalculationDataProvider(BaseCalculationDataProvider):
  def _provide_internal_calculation_data(self, client, assigned_entity):

    if not isinstance(assigned_entity, EngagementOpportunity):
      raise ValueError("This data provider only works with EO's")
    else:
      engagement_opportunity = assigned_entity

    ret_val = {}

    eo_attrs = engagement_opportunity.engagement_opportunity_attrs
    profile_attrs = engagement_opportunity.profile.profile_attrs

    ret_val[constants.BIO] = profile_attrs.get(constants.BIO)
    ret_val[constants.BIO_TA_TOPIC_SCORE_KEYWORD_MULTIPLIER] = 3

    ret_val[constants.NAME] = profile_attrs.get(constants.NAME)
    ret_val[constants.PROFILE_WEBSITES] = profile_attrs.get(constants.WEBSITES)
    ret_val[constants.LOCATION] = profile_attrs.get(constants.LOCATION)
    ret_val[constants.FOLLOWERS_COUNT] = profile_attrs.get(constants.FOLLOWERS_COUNT, 0)
    ret_val[constants.RECENT_POSTS] = profile_attrs.get(constants.RECENT_TWEETS)
    ret_val[constants.RECENT_POST_TA_TOPIC_SCORE_MULTIPLIER] = 1

    ret_val[constants.TEXT] = eo_attrs.get(constants.TEXT)
    ret_val[constants.TEXT_HTML] = eo_attrs.get(constants.TEXT_HTML)
    ret_val[constants.EO_WEBSITES] = eo_attrs.get(constants.WEBSITES)
    ret_val[constants.EO_WEBSITE_TA_TOPIC_KEYWORD_SCORE_MULTIPLIER] = 1

    ret_val[constants.CREATED_DATE] = engagement_opportunity.created_date

    ret_val[constants.SUBMISSION_OWNER] = True
    ret_val[constants.SUBMISSION_OWNER_SCORE_MULTIPLIER] = 0
    ret_val[constants.COMPANY] = profile_attrs.get(constants.COMPANY)
    ret_val[constants.COMPANY] = profile_attrs.get(constants.COMPANY)
    ret_val[constants.COMPANY_UNIVERSAL_NAME] = profile_attrs.get(constants.COMPANY_UNIVERSAL_NAME)
    ret_val[constants.COMPANY_INDUSTRIES] = profile_attrs.get(constants.COMPANY_INDUSTRIES)
    ret_val[constants.COMPANY_EMPLOYEE_COUNT] = profile_attrs.get(constants.COMPANY_EMPLOYEE_COUNT)
    ret_val[constants.COMPANY_INDUSTRY_SCORE] = profile_attrs.get(constants.COMPANY_INDUSTRY_SCORE)
    ret_val[constants.COMPANY_EMPLOYEE_COUNT_SCORE] = profile_attrs.get(constants.COMPANY_EMPLOYEE_COUNT_SCORE)

    return ret_val
