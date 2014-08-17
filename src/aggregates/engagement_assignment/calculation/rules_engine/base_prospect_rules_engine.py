from abc import ABC, abstractmethod
from collections import Counter
import logging
from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.calculation_objects import RulesEngineScoredObject
from src.libs.geo_utils.services import geo_location_service

logger = logging.getLogger(__name__)


class BaseProspectRulesEngine(ABC):
  def __init__(self, _geo_location_service=None):

    if not _geo_location_service: _geo_location_service = geo_location_service
    self._geo_location_service = _geo_location_service

  def score_it(self, prospect):
    prospect_internal_score, prospect_internal_score_attrs = self._get_internal_score(prospect)
    prospect_base_score, prospect_base_score_attrs = self._apply_base_score(prospect)

    ret_val = RulesEngineScoredObject(
      prospect_internal_score, prospect_internal_score_attrs,
      prospect_base_score, prospect_base_score_attrs
    )

    return ret_val

  def _apply_base_score(self, prospect):
    score, score_attrs = 0, {}

    location_score, location_score_attrs = self._apply_location_score(prospect)
    score += location_score
    score_attrs.update(location_score_attrs)

    return score, score_attrs


  def _apply_location_score(self, prospect):
    counter, score, score_attrs = self._get_default_score_items()

    location = prospect.prospect_attrs.get(constants.LOCATION)

    if location:
      location_score = 1

      try:
        country = self._geo_location_service.get_country(location)
      except:
        country = None

      if country:
        country = country.lower()
        for home_country in self._important_home_countries:
          if country in home_country:
            score += location_score
            counter[constants.LOCATION] += location_score

      location = location.lower()

      if any(loc in location for loc in self._important_locations):
        score += location_score
        # todo why are we storing a counter?it doesn't make sense if we only use one key in this dict. I guess it
        # maekse sense if we store one key for `City` and one for `State`.
        counter[constants.LOCATION] += location_score

      if counter[constants.LOCATION]: score_attrs[constants.LOCATION] = counter[constants.LOCATION]

    return score, score_attrs


  @abstractmethod
  def _get_internal_score(self, prospect):
    """Get the client-specific rules"""


  @property
  def _important_locations(self):
    return ()


  @property
  def _important_home_countries(self):
    return ()

  def _get_default_score_items(self):
    score, score_attrs, counter = 0, {}, Counter()
    return counter, score, score_attrs
