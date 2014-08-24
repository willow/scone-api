from abc import ABC
from collections import Counter
import logging


logger = logging.getLogger(__name__)


class BaseRulesEngine(ABC):
  def _get_default_score_items(self):
    score, score_attrs, counter = 0, {}, Counter()
    return score, score_attrs, counter
