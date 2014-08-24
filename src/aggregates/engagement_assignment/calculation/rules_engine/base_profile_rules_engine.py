from abc import ABC, abstractmethod
import logging
from src.aggregates.engagement_assignment import constants

from src.aggregates.engagement_assignment.calculation.calculation_objects import RulesEngineScoredObject
from src.aggregates.engagement_assignment.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.libs.python_utils.collections import iter_utils


logger = logging.getLogger(__name__)


class BaseProfileRulesEngine(BaseRulesEngine):
  def __init__(self, profile, calc_data, _iter_utils=None):
    if not _iter_utils: _iter_utils = iter_utils
    self._iter_utils = _iter_utils

    self.profile = profile

    self.calc_data = calc_data

  def score_it(self):
    profile_internal_score, profile_internal_score_attrs = self._get_internal_score()
    profile_base_score, profile_base_score_attrs = self._apply_base_score()

    ret_val = RulesEngineScoredObject(
      profile_internal_score, profile_internal_score_attrs,
      profile_base_score, profile_base_score_attrs
    )

    return ret_val

  @abstractmethod
  def _apply_base_score(self):
    """Get the client-specific rules"""


  @abstractmethod
  def _get_internal_score(self):
    """Get the client-specific rules"""


class BaseTwitterProfileRulesEngine(BaseProfileRulesEngine):
  def _apply_base_score(self):
    score, score_attrs = 0, {}

    recent_tweet_score, recent_tweet_score_attrs = self._apply_recent_tweets_score()
    score += recent_tweet_score
    score_attrs.update(recent_tweet_score_attrs)

    return score, score_attrs

  def _apply_recent_tweets_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    recent_tweets = self.profile.profile_attrs.get(constants.RECENT_TWEETS)

    if recent_tweets:

      client_topics = self.calc_data[constants.STEMMED_TA_TOPIC_KEYWORDS]

      recent_tweets_score = self._recent_tweets_score

      recent_tweets = self._iter_utils.stemmify_iterable(recent_tweets)

      for stemmed_topic_keyword in client_topics:
        for tweet in recent_tweets:
          if stemmed_topic_keyword in tweet:
            score += recent_tweets_score
            counter[constants.RECENT_TWEET_TA_TOPIC_KEYWORD_SCORE] += recent_tweets_score
            # give, at most, 1 point per topic mention
            break

      if counter[constants.RECENT_TWEET_TA_TOPIC_KEYWORD_SCORE]:

        x = constants.RECENT_TWEET_TA_TOPIC_KEYWORD_SCORE

        score_attrs[x] = counter[x]

    return score, score_attrs

  @property
  def _recent_tweets_score(self):
    return 1

class BaseRedditProfileRulesEngine(BaseProfileRulesEngine):
  def _apply_base_score(self):
    score, score_attrs = 0, {}

    recent_comments_score, recent_comments_score_attrs = self._apply_recent_comments_score()
    score += recent_comments_score
    score_attrs.update(recent_comments_score_attrs)

    return score, score_attrs

  def _apply_recent_comments_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    recent_comments = self.profile.profile_attrs.get(constants.RECENT_COMMENTS)

    if recent_comments:

      client_topics = self.calc_data[constants.STEMMED_TA_TOPIC_KEYWORDS]

      recent_comments_score = self._recent_comments_score

      recent_comments = self._iter_utils.stemmify_iterable(recent_comments)

      for stemmed_topic_keyword in client_topics:
        for comment in recent_comments:
          if stemmed_topic_keyword in comment:
            score += recent_comments_score
            counter[constants.RECENT_COMMENT_TA_TOPIC_KEYWORD_SCORE] += recent_comments_score
            # give, at most, 1 point per topic mention
            break

      if counter[constants.RECENT_COMMENT_TA_TOPIC_KEYWORD_SCORE]:

        x = constants.RECENT_COMMENT_TA_TOPIC_KEYWORD_SCORE

        score_attrs[x] = counter[x]

    return score, score_attrs

  @property
  def _recent_comments_score(self):
    return 1


class BaseLinkedInProfileRulesEngine(BaseProfileRulesEngine, ABC):
  def _apply_base_score(self):
    score, score_attrs = 0, {}

