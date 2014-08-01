from abc import ABC, abstractmethod
import logging
from src.aggregates.engagement_assignment.calculation.calculation_objects import RulesEngineScoredObject

logger = logging.getLogger(__name__)


class BaseEngagementOpportunityRulesEngine(ABC):
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
  def _apply_base_score(self, engagement_opportunity):
    """Get the client-specific rules"""


  @abstractmethod
  def _get_internal_score(self, engagement_opportunity):
    """Get the client-specific rules"""


class BaseTwitterEngagementOpportunityRulesEngine(BaseEngagementOpportunityRulesEngine, ABC):
  def _apply_base_score(self, engagement_opportunity):
    return 0, {}


class BaseRedditEngagementOpportunityRulesEngine(BaseEngagementOpportunityRulesEngine, ABC):
  def _apply_base_score(self, engagement_opportunity):
    return 0, {}


class BaseLinkedInEngagementOpportunityRulesEngine(BaseEngagementOpportunityRulesEngine, ABC):
  def _apply_base_score(self, engagement_opportunity):
    return 0, {}
