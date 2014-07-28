from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.calculation_data_providers.base_calculation_data_provider import \
  BaseCalculationDataProvider
from src.aggregates.profile.models import Profile


class LinkedinCalculationDataProvider(BaseCalculationDataProvider):
  def _provide_internal_calculation_data(self, client, assigned_entity):

    if not isinstance(assigned_entity, Profile):
      raise ValueError("This data provider only works with Profiles's")
    else:
      profile = assigned_entity

    ret_val = {}

    profile_attrs = profile.profile_attrs

    ret_val[constants.NAME] = profile_attrs.get(constants.NAME)
    ret_val[constants.BIO] = profile_attrs.get(constants.BIO)
    ret_val[constants.BIO_TA_TOPIC_SCORE_KEYWORD_MULTIPLIER] = 0

    ret_val[constants.RECENT_POSTS] = []
    ret_val[constants.RECENT_POST_TA_TOPIC_SCORE_MULTIPLIER] = 2
    ret_val[constants.TEXT] = profile_attrs.get(constants.TEXT)
    ret_val[constants.TEXT_HTML] = profile_attrs.get(constants.TEXT_HTML)
    ret_val[constants.EO_WEBSITES] = profile_attrs.get(constants.WEBSITES)
    ret_val[constants.EO_WEBSITE_TA_TOPIC_KEYWORD_SCORE_MULTIPLIER] = 3

    ret_val[constants.PROFILE_WEBSITES] = profile_attrs.get(constants.PROFILE_WEBSITES)
    ret_val[constants.CREATED_DATE] = profile.system_created_date

    location = profile_attrs.get(constants.LOCATION)
    if location:
      ret_val[constants.LOCATION] = location['name']
    else:
      ret_val[constants.LOCATION] = None

    ret_val[constants.SUBMISSION_OWNER] = True
    ret_val[constants.SUBMISSION_OWNER_SCORE_MULTIPLIER] = 0

    ret_val[constants.FOLLOWERS_COUNT] = profile_attrs.get(constants.FOLLOWERS_COUNT)

    company = profile_attrs.get(constants.COMPANY)
    if company:
      company_data = {}

      company_employee_count = company.get(constants.COMPANY_EMPLOYEE_COUNT)

      if company_employee_count:
        try:
          employee_count = int(company_employee_count.split("-")[1])
          company_data[constants.COMPANY_EMPLOYEE_COUNT] = employee_count
        except:
          company_data[constants.COMPANY_EMPLOYEE_COUNT] = None
      else:
        company_data[constants.COMPANY_EMPLOYEE_COUNT] = None

      industries = company.get(constants.COMPANY_INDUSTRIES)
      if industries:
        company_data[constants.COMPANY_INDUSTRIES] = industries
      else:
        company_data[constants.COMPANY_INDUSTRIES] = None

      if company_data:
        ret_val[constants.COMPANY] = company_data

    else:
      ret_val[constants.COMPANY] = None

    return ret_val
