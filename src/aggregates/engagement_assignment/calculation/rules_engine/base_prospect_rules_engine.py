from abc import abstractmethod
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import logging

from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.calculation_objects import RulesEngineScoredObject
from src.aggregates.engagement_assignment.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.apps.domain.engagement_assignment.services import assigned_prospect_service
from src.libs.datetime_utils.parsers import datetime_parser
from src.libs.geo_utils.services import geo_location_service
from src.libs.nlp_utils.services.enums import GenderEnum
from src.libs.python_utils.collections import iter_utils


logger = logging.getLogger(__name__)


class BaseProspectRulesEngine(BaseRulesEngine):
  def __init__(
      self, prospect, calc_data,
      _geo_location_service=None, _iter_utils=None, _assigned_prospect_service=None, _datetime_parser=None):

    self.prospect = prospect
    self.calc_data = calc_data

    if not _geo_location_service: _geo_location_service = geo_location_service
    self._geo_location_service = _geo_location_service

    if not _iter_utils: _iter_utils = iter_utils
    self._iter_utils = _iter_utils

    if not _assigned_prospect_service: _assigned_prospect_service = assigned_prospect_service
    self._assigned_prospect_service = _assigned_prospect_service

    if not _datetime_parser: _datetime_parser = datetime_parser
    self._datetime_parser = _datetime_parser

  def score_it(self):
    prospect_internal_score, prospect_internal_score_attrs = self._get_internal_score()
    prospect_base_score, prospect_base_score_attrs = self._apply_base_score()

    ret_val = RulesEngineScoredObject(
      prospect_internal_score, prospect_internal_score_attrs,
      prospect_base_score, prospect_base_score_attrs
    )

    return ret_val

  def _apply_base_score(self):
    score, score_attrs = 0, {}

    location_score, location_score_attrs = self._apply_location_score()
    score += location_score
    score_attrs.update(location_score_attrs)

    age_score, age_score_attrs = self._apply_age_score()
    score += age_score
    score_attrs.update(age_score_attrs)

    gender_score, gender_score_attrs = self._apply_gender_score()
    score += gender_score
    score_attrs.update(gender_score_attrs)

    bio_score, bio_score_attrs = self._apply_bio_score()
    score += bio_score
    score_attrs.update(bio_score_attrs)

    website_score, website_score_attrs = self._apply_website_score()
    score += website_score
    score_attrs.update(website_score_attrs)

    email_score, email_score_attrs = self._apply_email_score()
    score += email_score
    score_attrs.update(email_score_attrs)

    prospect_assignment_score, prospect_assignment_score_attrs = self._apply_prospect_assignment_score()
    score += prospect_assignment_score
    score_attrs.update(prospect_assignment_score_attrs)

    return score, score_attrs

  # region apply score logic

  def _apply_location_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    location = self.prospect.prospect_attrs.get(constants.LOCATION)

    if location:
      location_score = self._location_score

      try:
        country = self._geo_location_service.get_country(location)
      except:
        country = None

      if country:
        country = country.lower()
        for home_country in self._important_home_countries:
          if country in home_country:
            score += location_score
            counter[constants.LOCATION_SCORE] += location_score

      location = location.lower()

      if any(loc in location for loc in self._important_locations):
        score += location_score
        counter[constants.LOCATION_SCORE] += location_score

      if counter[constants.LOCATION_SCORE]: score_attrs[constants.LOCATION_SCORE] = counter[constants.LOCATION_SCORE]

    return score, score_attrs

  def _apply_age_score(self):
    score, score_attrs, counter = self._get_default_score_items()
    age = self.prospect.prospect_attrs.get(constants.RELATIVE_DOB)

    age_min, age_max = self._age_range

    if age_min and age_max:
      if age:
        age = self._datetime_parser.get_datetime(age)

        age_years = relativedelta(timezone.now(), age).years

        if age_min <= age_years <= age_max:
          age_score = self._age_score
          score += age_score

          counter[constants.RELATIVE_DOB_SCORE] += age_score

          if counter[constants.RELATIVE_DOB_SCORE]:
            score_attrs[constants.RELATIVE_DOB_SCORE] = counter[constants.RELATIVE_DOB_SCORE]

    return score, score_attrs

  def _apply_gender_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    gender = self.prospect.prospect_attrs.get(constants.GENDER)

    preferred_gender = self._preferred_gender

    if preferred_gender:
      if gender:

        gender = GenderEnum[gender.lower()]

        if gender == preferred_gender:
          gender_score = self._gender_score
          score += gender_score
          score_attrs[constants.GENDER_SCORE] = gender_score

    return score, score_attrs

  def _apply_bio_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    bio = self.prospect.prospect_attrs.get(constants.BIO)

    if bio:
      bio = self._iter_utils.stemmify_string(bio)

      # region client topic
      client_topics = self.calc_data[constants.STEMMED_TA_TOPIC_KEYWORDS]
      if client_topics:
        bio_client_topic_score = self._bio_client_topic_score

        for stemmed_topic_keyword in client_topics:
          if stemmed_topic_keyword in bio:
            score += bio_client_topic_score
            counter[constants.BIO_CLIENT_TA_TOPIC_SCORE] += bio_client_topic_score

        if counter[constants.BIO_CLIENT_TA_TOPIC_SCORE]:
          score_attrs[constants.BIO_CLIENT_TA_TOPIC_SCORE] = counter[constants.BIO_CLIENT_TA_TOPIC_SCORE]

      "pycharm doesn't recognize endregion"
      # endregion client topic

      # region important keywords
      bio_keywords = self._important_bio_keywords

      if bio_keywords:
        bio_keywords = self._iter_utils.stemmify_iterable(bio_keywords)

        bio_score = self._bio_important_keyword_score

        for kw in bio_keywords:
          if kw in bio:
            score += bio_score
            counter[constants.BIO_IMPORTANT_KEYWORD_SCORE] += bio_score

        if counter[constants.BIO_IMPORTANT_KEYWORD_SCORE]:
          score_attrs[constants.BIO_IMPORTANT_KEYWORD_SCORE] = counter[constants.BIO_IMPORTANT_KEYWORD_SCORE]

      "pycharm doesn't recognize endregion"
      # endregion important keywords

      # region avoid keywords
      bio_keywords = self._important_bio_keywords

      if bio_keywords:
        bio_keywords = self._iter_utils.stemmify_iterable(bio_keywords)

        bio_score = self._bio_important_keyword_score

        avoid_words = self.calc_data[constants.PROFANITY_FILTER_WORDS]

        avoid_words += self._bio_avoid_keywords

        avoid_words = self._iter_utils.stemmify_iterable(avoid_words)

        for kw in bio_keywords:
          if kw in avoid_words:
            score += bio_score
            counter[constants.BIO_AVOID_KEYWORD_SCORE] += bio_score

        if counter[constants.BIO_AVOID_KEYWORD_SCORE]:
          score_attrs[constants.BIO_AVOID_KEYWORD_SCORE] = counter[constants.BIO_AVOID_KEYWORD_SCORE]

      "pycharm doesn't recognize endregion"
      # endregion avoid keywords

    return score, score_attrs

  def _apply_website_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    websites = self.prospect.prospect_attrs.get(constants.WEBSITES)

    important_websites = self._important_websites

    if important_websites:

      if websites:

        website_score = self._website_score

        for ws in important_websites:
          if any(domain in ws.lower() for domain in self._important_websites):
            score += website_score
            counter[constants.WEBSITES_SCORE] += website_score

        if counter[constants.WEBSITES_SCORE]:
          score_attrs[constants.WEBSITES_SCORE] = counter[constants.WEBSITES_SCORE]

    return score, score_attrs

  def _apply_email_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    email_addresses = self.prospect.prospect_attrs.get(constants.EMAIL_ADDRESSES)

    if email_addresses:
      score += self._email_score
      counter[constants.EMAIL_ADDRESSES_SCORE] += self._email_score

    if counter[constants.EMAIL_ADDRESSES_SCORE]:
      score_attrs[constants.EMAIL_ADDRESSES_SCORE] = counter[constants.EMAIL_ADDRESSES_SCORE]

    return score, score_attrs


  def _apply_prospect_assignment_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    client_uid = self.calc_data[constants.CLIENT_UID]
    prospect_uid = self.prospect.prospect_uid

    try:
      self._assigned_prospect_service.get_assigned_prospect_from_attrs(client_uid, prospect_uid)
    except:
      new_prospect_score = self._new_prospect_score
      score += new_prospect_score
      score_attrs[constants.NEW_PROSPECT_SCORE] = new_prospect_score
      logger.debug("new assigned prospect. client_uid: %s prospect_uid: %s", client_uid, prospect_uid)
    else:
      logger.debug("existing assigned prospect. client_uid: %s prospect_uid: %s", client_uid, prospect_uid)

    return score, score_attrs

  # endregion apply score logic

  @abstractmethod
  def _get_internal_score(self):
    """Get the client-specific rules"""

  # region define prospect scoring attrs

  @property
  def _important_locations(self):
    return ()

  @property
  def _location_score(self):
    return 1

  @property
  def _important_home_countries(self):
    return ()

  @property
  def _age_range(self):
    return (None, None)

  @property
  def _age_score(self):
    return 1

  @property
  def _preferred_gender(self):
    return None

  @property
  def _gender_score(self):
    return 1

  @property
  def _important_bio_keywords(self):
    return ()

  @property
  def _bio_important_keyword_score(self):
    return 1

  @property
  def _bio_client_topic_score(self):
    return 1

  @property
  def _important_websites(self):
    return ()

  @property
  def _website_score(self):
    return 1

  @property
  def _email_score(self):
    return 1

  @property
  def _new_prospect_score(self):
    return 1

  @property
  def _bio_avoid_keywords(self):
    return ()

  @property
  def _bio_avoid_keyword_score(self):
    return -1

  "pycharm recognize region"
  # endregion define prospect scoring attrs
