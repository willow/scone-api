from abc import abstractmethod
import logging

from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.calculation_objects import RulesEngineScoredObject
from src.aggregates.engagement_assignment.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.libs.python_utils.collections import iter_utils


logger = logging.getLogger(__name__)


class BaseEngagementOpportunityRulesEngine(BaseRulesEngine):
  def __init__(self, engagement_opportunity, calc_data, _iter_utils=None):
    if not _iter_utils: _iter_utils = iter_utils
    self._iter_utils = _iter_utils

    self.engagement_opportunity = engagement_opportunity
    self.calc_data = calc_data


  def score_it(self, engagement_opportunity):
    engagement_opportunity_internal_score, engagement_opportunity_internal_score_attrs = self._get_internal_score(
      engagement_opportunity)
    engagement_opportunity_base_score, engagement_opportunity_base_score_attrs = self._apply_base_score(
      engagement_opportunity)

    ret_val = RulesEngineScoredObject(
      engagement_opportunity_internal_score, engagement_opportunity_internal_score_attrs,
      engagement_opportunity_base_score, engagement_opportunity_base_score_attrs
    )

    return ret_val

  @abstractmethod
  def _apply_base_score(self):
    """Get the client-specific rules"""


  @abstractmethod
  def _get_internal_score(self):
    """Get the client-specific rules"""


class BaseTwitterEngagementOpportunityRulesEngine(BaseEngagementOpportunityRulesEngine):
  def _apply_base_score(self):
    score, score_attrs = 0, {}

    recent_tweet_score, recent_tweet_score_attrs = self._apply_tweet_text_score()
    score += recent_tweet_score
    score_attrs.update(recent_tweet_score_attrs)

    return score, score_attrs

  def _apply_tweet_text_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    tweet_text = self.engagement_opportunity.engagement_opportunity_attrs.get(constants.TEXT)

    if tweet_text:

      tweet_text_ta_topic_score = self._text_tweet_ta_topic_score

      client_topics = self.calc_data[constants.STEMMED_TA_TOPIC_KEYWORDS]

      tweet_text = self._iter_utils.stemmify_string(tweet_text)

      for stemmed_topic_keyword in client_topics:
          if stemmed_topic_keyword in tweet_text:
            score += tweet_text_ta_topic_score
            counter[constants.TWEET_TEXT_TA_TOPIC_KEYWORD_SCORE] += tweet_text_ta_topic_score
            # give, at most, 1 point per topic mention
            break

      if counter[constants.TWEET_TEXT_TA_TOPIC_KEYWORD_SCORE]:
        x = constants.TWEET_TEXT_TA_TOPIC_KEYWORD_SCORE

        score_attrs[x] = counter[x]

    return score, score_attrs

  @property
  def _text_tweet_ta_topic_score(self):
    return 1


class BaseRedditEngagementOpportunityRulesEngine(BaseEngagementOpportunityRulesEngine):
  def _apply_base_score(self):
    return 0, {}


class BaseLinkedInEngagementOpportunityRulesEngine(BaseEngagementOpportunityRulesEngine):
  def _apply_base_score(self):
    return 0, {}
