import logging

from src.aggregates.profile import constants
from src.libs.python_utils.logging.logging_utils import log_wrapper
from src.libs.social_utils.providers.linkedin import linkedin_client_service
from src.libs.social_utils.providers.linkedin.linkedin_client_service import get_linkedin_view_id, \
  get_linkedin_public_url


logger = logging.getLogger(__name__)


def get_linkedin_profile_attrs(profile_external_id, **kwargs):
  return _get_linkedin_profile_data(profile_external_id, **kwargs)


def _get_linkedin_profile_data(profile_external_id, _linkedin_client_service=None, **kwargs):
  if not _linkedin_client_service: _linkedin_client_service = linkedin_client_service

  log_message = (
    "Get linkedin profile data. linkedin_id: %s",
    profile_external_id
  )

  with log_wrapper(logger.debug, *log_message):

    # https://developer.linkedin.com/documents/profile-fields
    fields = [
      'id',
      'formatted-name',
      'headline',
      'location:(name)',
      'positions:(company:(id))',
      'industry',
      'relation-to-viewer:(related-connections)',
      'num-connections',
      'summary',
      'specialties',
      'picture-url',
      'public-profile-url',
    ]

    user = _linkedin_client_service.get_linkedin_profile_data_from_id(profile_external_id, fields)

    profile_url = user.get('publicProfileUrl')
    name = user.get('formattedName')
    summary = user.get('summary')
    title = user.get('title')
    location = user.get('location')
    number_of_connecetions = user.get('num-connections')

    if not profile_url:
      # this can happen if their data is set to private
      profile_url = get_linkedin_public_url(profile_external_id)

    linkedin_view_id = get_linkedin_view_id(profile_url)

    linkedin_profile_data = {}

    if profile_url: linkedin_profile_data[constants.PROFILE_URL] = profile_url
    if name: linkedin_profile_data[constants.NAME] = name
    if summary: linkedin_profile_data[constants.TEXT] = summary
    if title: linkedin_profile_data[constants.TITLE] = title
    if location: linkedin_profile_data[constants.LOCATION] = location
    if number_of_connecetions: linkedin_profile_data[constants.NUMBER_OF_CONNECTIONS] = number_of_connecetions

    linkedin_profile_data[constants.LINKEDIN_VIEW_ID] = linkedin_view_id

    positions = user.get('positions')
    if positions:
      try:
        company_id = positions["values"][0]["company"]["id"]

        company_fields = [
          'universal-name',
          'industries:(name)',
          'employee-count-range:(name)',
          'specialties',
        ]

        company = _linkedin_client_service.get_linkedin_company_data_from_id(company_id, company_fields)
        company_data = {}
        universal_name = company.get('universalName')

        industries = company.get('industries')
        industry_names = None
        if industries:
          industry_names = [i['name'] for i in industries['values']]

        employee_count = company.get('employeeCountRange')

        if universal_name: company_data[constants.COMPANY_UNIVERSAL_NAME] = universal_name
        if industry_names: company_data[constants.COMPANY_INDUSTRIES] = industry_names

        if employee_count:
          employee_count = employee_count['name']
          company_data[constants.COMPANY_EMPLOYEE_COUNT] = employee_count

        if company_data: linkedin_profile_data[constants.COMPANY] = company_data
      except:
        pass

    topic_ids = kwargs.get(constants.TOPIC_IDS)

    if topic_ids:
      linkedin_profile_data[constants.TOPIC_IDS] = topic_ids

  return linkedin_profile_data
