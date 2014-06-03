from collections import Counter
from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.libs.geo_utils.services import geo_location_service
from src.libs.python_utils.collections import iter_utils
from src.libs.text_utils.parsers import text_parser


class TechStartupRulesEngine(BaseRulesEngine):
  _important_websites = (
    "linkedin",
    "wordpress",
    "blogspot",
    "about.me",
    "ycombinator",
    "stackoverflow",
    ".io",
  )

  _important_bio_keywords = iter_utils.stemmify_iterable((
    "ceo",
    "cto",
    "software",
    "developer",
    "engineer",
    "programmer",
    "writer",
    "founder",
    "startup",
  ))

  _important_locations = (
    "sf",
    "san fran",
    "nyc",
    "new york",
  )
  
  _home_countries = (
    "united states",
  )

  def _get_internal_score(self, calculation_data, _iter_utils=iter_utils, _geolocation_service=geo_location_service, 
                          _text_parser = text_parser):
    score = 0
    internal_score_attrs = {}
    counter = Counter()

    profile_websites = calculation_data[constants.PROFILE_WEBSITES]
    if profile_websites:
      website_score = 1
      for ws in profile_websites:
        if any(domain in ws.lower() for domain in self._important_websites):
          score += website_score
          counter[constants.PROFILE_WEBSITES] += website_score
      if counter[constants.PROFILE_WEBSITES]: internal_score_attrs[constants.PROFILE_WEBSITES] = counter[constants.PROFILE_WEBSITES]

    bio = calculation_data[constants.BIO]
    if bio:
      bio_score = 1
      bio = _iter_utils.stemmify_string(bio)
      for kw in self._important_bio_keywords:
        if kw in bio:
          score += bio_score
          counter[constants.BIO] += bio_score
      if counter[constants.BIO]: internal_score_attrs[constants.BIO] = counter[constants.BIO]

    followers_count = calculation_data[constants.FOLLOWERS_COUNT]
    if followers_count and followers_count >= 2500:
      followers_count_score = 1
      score += followers_count_score
      internal_score_attrs[constants.FOLLOWERS_COUNT] = followers_count_score

    location = calculation_data[constants.LOCATION]
    if location:
      location_score = 1
      country = _geolocation_service.get_country(location).lower()
      for home_country in self._home_countries:
        if country in home_country:
          score += location_score
          counter[constants.LOCATION] += location_score

      location = location.lower()
      if any(loc in location for loc in self._important_locations):
        score += location_score
        counter[constants.LOCATION] += location_score

      if counter[constants.LOCATION]: internal_score_attrs[constants.LOCATION] = counter[constants.LOCATION]

    internal_score_attrs[constants.SCORE] = score

    return score, internal_score_attrs
