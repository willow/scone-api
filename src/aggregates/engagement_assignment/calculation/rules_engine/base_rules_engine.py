from abc import ABC, abstractmethod
from collections import Counter
from datetime import datetime
from pytz import UTC
from src.aggregates.engagement_assignment import constants
from src.apps.domain.engagement_assignment.services import assigned_prospect_service
from src.libs.python_utils.collections import iter_utils
from src.libs.text_utils.parsers import text_parser
from src.libs.web_utils.scraping import scraper_utils
import logging

epoch = datetime(1970, 1, 1, tzinfo=UTC)

logger = logging.getLogger(__name__)


class BaseRulesEngine(ABC):
  def apply_base_score(
      self, calculation_data, _iter_utils=iter_utils, _text_parser=text_parser,
      _assigned_prospect_service=assigned_prospect_service):
    score = 0
    base_score_attrs = {}
    counter = Counter()

    bio = calculation_data[constants.BIO]
    if bio:
      bio_score = 1
      score += bio_score
      base_score_attrs[constants.BIO] = bio_score

    emails = calculation_data[constants.EMAIL_ADDRESSES]
    if emails:
      email_score = 1
      score += email_score
      base_score_attrs[constants.EMAIL_ADDRESSES] = email_score

    stemmed_keywords = calculation_data[constants.STEMMED_TA_TOPIC_KEYWORDS]
    text = calculation_data[constants.TEXT]
    if text:
      text = _iter_utils.stemmify_string(text)
      text_ta_topic_keyword_score = 1
      for stemmed_keyword in stemmed_keywords:
        if stemmed_keyword in text:
          score += text_ta_topic_keyword_score
          counter[constants.TEXT_TA_TOPIC_KEYWORD_SCORE] += text_ta_topic_keyword_score
      if counter[constants.TEXT_TA_TOPIC_KEYWORD_SCORE]:
        base_score_attrs[constants.TEXT_TA_TOPIC_KEYWORD_SCORE] = counter[constants.TEXT_TA_TOPIC_KEYWORD_SCORE]

    bio = calculation_data[constants.BIO]
    if bio:
      bio_ta_topic_score = 1 * calculation_data[constants.BIO_TA_TOPIC_SCORE_KEYWORD_MULTIPLIER]
      bio = _iter_utils.stemmify_string(bio)
      for stemmed_keyword in stemmed_keywords:
        if stemmed_keyword in bio:
          score += bio_ta_topic_score
          counter[constants.BIO_TA_TOPIC_KEYWORD_SCORE] += bio_ta_topic_score

      if counter[constants.BIO_TA_TOPIC_KEYWORD_SCORE]: base_score_attrs[constants.BIO_TA_TOPIC_KEYWORD_SCORE] = \
        counter[
          constants.BIO_TA_TOPIC_KEYWORD_SCORE]

    submission_owner = calculation_data[constants.SUBMISSION_OWNER]
    if submission_owner:
      submission_owner_score = 1 * calculation_data[constants.SUBMISSION_OWNER_SCORE_MULTIPLIER]
      score += submission_owner_score
      counter[constants.SUBMISSION_OWNER_SCORE] += submission_owner_score

      if counter[constants.SUBMISSION_OWNER_SCORE]: base_score_attrs[constants.SUBMISSION_OWNER_SCORE] = counter[
        constants.SUBMISSION_OWNER_SCORE]

    recent_posts = calculation_data[constants.RECENT_POSTS]
    if recent_posts:
      recent_post_ta_topic_score = 1 * calculation_data[constants.RECENT_POST_TA_TOPIC_SCORE_MULTIPLIER]
      recent_posts = _iter_utils.stemmify_iterable(recent_posts)
      for stemmed_keyword in stemmed_keywords:
        for post in recent_posts:
          if stemmed_keyword in post:
            score += recent_post_ta_topic_score
            counter[constants.RECENT_POST_TA_TOPIC_KEYWORD_SCORE] += recent_post_ta_topic_score
            # give, at most, 1 point per topic mention
            break

      if counter[constants.RECENT_POST_TA_TOPIC_KEYWORD_SCORE]:
        base_score_attrs[constants.RECENT_POST_TA_TOPIC_KEYWORD_SCORE] = counter[
          constants.RECENT_POST_TA_TOPIC_KEYWORD_SCORE]

    eo_websites = calculation_data[constants.EO_WEBSITES]
    if eo_websites:
      eo_website_ta_topic_score = 1 * calculation_data[constants.EO_WEBSITE_TA_TOPIC_KEYWORD_SCORE_MULTIPLIER]
      for eo_website in eo_websites:
        try:
          content = scraper_utils.get_main_content_from_web_page(eo_website[constants.URL])
          content = _text_parser.strip_html(content)
          content = _iter_utils.stemmify_string(content)
          for stemmed_keyword in stemmed_keywords:
            if stemmed_keyword in content:
              score += eo_website_ta_topic_score
              counter[constants.EO_WEBSITE_TA_TOPIC_KEYWORD_SCORE] += eo_website_ta_topic_score
        except Exception:
          logger.debug("Error summarizing websites", exc_info=True)
          continue

      if counter[constants.EO_WEBSITE_TA_TOPIC_KEYWORD_SCORE]:
        base_score_attrs[constants.EO_WEBSITE_TA_TOPIC_KEYWORD_SCORE] = counter[
          constants.EO_WEBSITE_TA_TOPIC_KEYWORD_SCORE]

    client_uid = calculation_data[constants.CLIENT_UID]
    prospect_uid = calculation_data[constants.PROSPECT_UID]

    try:
      _assigned_prospect_service.get_assigned_prospect_from_attrs(client_uid, prospect_uid)
    except:
      new_prospect_score = 5
      score += new_prospect_score
      base_score_attrs[constants.NEW_PROSPECT_SCORE] = new_prospect_score
      logger.debug("new assigned prospect. client_uid: %s prospect_uid: %s", client_uid, prospect_uid)
    else:
      logger.debug("existing assigned prospect. client_uid: %s prospect_uid: %s", client_uid, prospect_uid)

    base_score_attrs[constants.SCORE] = score

    return score, base_score_attrs

  def get_score(self, calculation_data):
    internal_score, internal_score_attrs = self._get_internal_score(calculation_data)

    base_score, base_score_attrs = self.apply_base_score(calculation_data)

    eo_created_date = calculation_data[constants.CREATED_DATE]

    score = base_score + internal_score

    score = self.rank(score, eo_created_date)

    pre_score = internal_score_attrs[constants.SCORE] + base_score_attrs[constants.SCORE]

    score_attrs = {
      'pre_score': pre_score, 'base_score_attrs': base_score_attrs,
      'internal_score_attrs': internal_score_attrs
    }

    return score, score_attrs


  @staticmethod
  def epoch_seconds(date):
    """Returns the number of seconds from the epoch to date."""
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


  @staticmethod
  def rank(score, date):
    seconds = BaseRulesEngine.epoch_seconds(date) - 1398984357
    return round(score + seconds / 1000000, 7)


  @abstractmethod
  def _get_internal_score(self, calculation_data):
    """Get the client-specific rules"""

  @abstractmethod
  def get_final_score(self, score_attrs):
    """Get the client-specific score"""
