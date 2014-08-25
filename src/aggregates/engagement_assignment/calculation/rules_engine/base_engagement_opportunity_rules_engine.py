from abc import ABC, abstractmethod
import logging

from src.aggregates.engagement_assignment.calculation.calculation_objects import RulesEngineScoredObject
from src.aggregates.engagement_assignment.calculation.rules_engine.base_rules_engine import BaseRulesEngine


logger = logging.getLogger(__name__)


class BaseEngagementOpportunityRulesEngine(BaseRulesEngine):
  def __init__(self, engagement_opportunity, calc_data):
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

    recent_tweet_score, recent_tweet_score_attrs = self._apply_recent_tweets_score()
    score += recent_tweet_score
    score_attrs.update(recent_tweet_score_attrs)

    return score, score_attrs


class BaseRedditEngagementOpportunityRulesEngine(BaseEngagementOpportunityRulesEngine):
  def _apply_base_score(self):
    return 0, {}


class BaseLinkedInEngagementOpportunityRulesEngine(BaseEngagementOpportunityRulesEngine):
  def _apply_base_score(self):
    return 0, {}
