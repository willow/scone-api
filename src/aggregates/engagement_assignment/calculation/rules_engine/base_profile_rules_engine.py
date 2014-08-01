from abc import ABC, abstractmethod
import logging
from src.aggregates.engagement_assignment.calculation.calculation_objects import RulesEngineScoredObject

logger = logging.getLogger(__name__)


class BaseProfileRulesEngine(ABC):
  def score_it(self, profile):
    profile_internal_score, profile_internal_score_attrs = self._get_internal_score(profile)
    profile_base_score, profile_base_score_attrs = self._apply_base_score(profile)

    ret_val = RulesEngineScoredObject(
      profile_internal_score, profile_internal_score_attrs,
      profile_base_score, profile_base_score_attrs
    )

    return ret_val

  @abstractmethod
  def _apply_base_score(self, profile):
    """Get the client-specific rules"""


  @abstractmethod
  def _get_internal_score(self, profile):
    """Get the client-specific rules"""


class BaseTwitterProfileRulesEngine(BaseProfileRulesEngine, ABC):
  def _apply_base_score(self, profile):
    return 0, {}


class BaseRedditProfileRulesEngine(BaseProfileRulesEngine, ABC):
  def _apply_base_score(self, profile):
    return 0, {}


class BaseLinkedInProfileRulesEngine(BaseProfileRulesEngine, ABC):
  def _apply_base_score(self, profile):
    return 0, {}
