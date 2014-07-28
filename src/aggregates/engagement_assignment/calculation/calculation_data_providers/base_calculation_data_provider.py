from abc import ABC, abstractmethod
from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_opportunity.models import EngagementOpportunity
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.models import Profile
from src.aggregates.profile.services import profile_service
from src.aggregates.topic.enums import TopicCategoryEnum
from src.libs.datetime_utils.parsers.datetime_parser import get_datetime
from src.libs.nlp_utils.services.enums import GenderEnum


class BaseCalculationDataProvider(ABC):
  def _provide_birth_date(self, prospect, ret_val):
    ret_val[constants.RELATIVE_DOB] = (prospect.prospect_attrs or {}).get(constants.RELATIVE_DOB)

  def _provide_gender(self, prospect, ret_val):
    gender = (prospect.prospect_attrs or {}).get(constants.GENDER)

    if gender:
      gender = GenderEnum[gender.lower()]

    ret_val[constants.GENDER] = gender

  def _provide_employment_latest_start_date(self, prospect, ret_val):
    ret_val[constants.ORGANIZATION_LATEST_START_DATE] = None

    employments = (prospect.prospect_attrs or {}).get(constants.ORGANIZATIONS)
    if employments:
      latest_start_date = None
      for emp in employments:
        try:
          start_date = get_datetime(emp[constants.ORGANIZATION_START_DATE])
          if latest_start_date:
            if start_date > latest_start_date:
              latest_start_date = start_date
          else:
            latest_start_date = start_date
        except:
          pass
      if latest_start_date:
        ret_val[constants.ORGANIZATION_LATEST_START_DATE] = latest_start_date

  def _provide_stemmed_keywords(self, client, assigned_entity, ret_val):
    if isinstance(assigned_entity, Profile):
      profile = assigned_entity
      profile_attrs = profile.profile_attrs or {}
      topic_ids = profile_attrs.get(constants.TOPIC_IDS)
    elif isinstance(assigned_entity, EngagementOpportunity):
      eo = assigned_entity
      topic_ids = list(eo.topics.values_list('topic_type_id', flat=True))
    else:
      topic_ids = []

    ret_val[constants.STEMMED_TA_TOPIC_KEYWORDS] = [ta_topic.topic_type.snowball_stem for ta_topic in
                                                    client.ta_topics.exclude(topic_type_id__in=topic_ids)]
    stemmed_topic_keywords = []
    for ta_topic in client.ta_topics.exclude(topic_type_id__in=topic_ids):
      for keywords_topic in ta_topic.topic_type.subtopics.filter(category_type=TopicCategoryEnum.keywords):
        stemmed_topic_keywords.append(keywords_topic.subtopic_attrs[constants.SNOWBALL_STEM])
    if stemmed_topic_keywords:
      ret_val[constants.STEMMED_TA_TOPIC_KEYWORDS].extend(stemmed_topic_keywords)


  def _provide_base_calculation_data(self, client, assigned_entity):
    ret_val = {}

    prospect = self._get_prospect(assigned_entity)

    self._provide_birth_date(prospect, ret_val)

    self._provide_gender(prospect, ret_val)

    self._provide_employment_latest_start_date(prospect, ret_val)

    self._provide_email(prospect, ret_val)

    self._provide_stemmed_keywords(client, assigned_entity, ret_val)

    self._provide_client_data(client, ret_val)

    self._provide_prospect_data(prospect, ret_val)

    return ret_val


  def provide_calculation_data(self, client, assigned_entity):
    ret_val = self._provide_internal_calculation_data(client, assigned_entity)
    # todo: some providers return constants (like company_industry) - all providers should uniformly return the
    # same data
    base_data = self._provide_base_calculation_data(client, assigned_entity)

    ret_val.update(base_data)

    return ret_val


  @abstractmethod
  def _provide_internal_calculation_data(self, client, assigned_entity):
    """Get the client-specific rules"""


  def _provide_email(self, prospect, ret_val):
    prospect_attrs = prospect.prospect_attrs or {}

    emails = prospect_attrs.get(constants.EMAIL_ADDRESSES)

    ret_val[constants.EMAIL_ADDRESSES] = emails

  def _get_prospect(self, assigned_entity):
    if isinstance(assigned_entity, EngagementOpportunity):
      assigned_entity = engagement_opportunity_service.get_engagement_opportunity(assigned_entity.id)
      prospect = assigned_entity.profile.prospect
    elif isinstance(assigned_entity, Profile):
      assigned_entity = profile_service.get_profile(assigned_entity.id)
      prospect = assigned_entity.prospect
    else:
      raise ValueError("Invalid assignment attrs")

    return prospect

  def _provide_client_data(self, client, ret_val):
    ret_val[constants.CLIENT_UID] = client.client_uid

  def _provide_prospect_data(self, prospect, ret_val):
    ret_val[constants.PROSPECT_UID] = prospect.prospect_uid
