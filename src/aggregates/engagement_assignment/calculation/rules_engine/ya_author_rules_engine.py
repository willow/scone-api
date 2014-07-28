from collections import Counter
from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.libs.nlp_utils.services import demography_service
from src.libs.nlp_utils.services.enums import GenderEnum
from src.libs.python_utils.collections import iter_utils
from src.libs.text_utils.parsers import text_parser


class YAAuthorRulesEngine(BaseRulesEngine):
  def __init__(self, _demography_service=demography_service):
    super().__init__()
    self._demography_service = _demography_service

  _important_websites = (
    "goodreads",
    "wordpress",
    "blogspot",
    "about.me",
    "pinterest",
  )

  _important_bio_keywords = iter_utils.stemmify_iterable((
    "#ya",
    "#youngadult",
    "young adult",
    "reader",
    "fan fic",
    "book",
    "fantasy",
    "writer",
  ))

  _important_locations = (
    "sf",
    "san fran",
    "nyc",
    "new york",
  )

  def _get_internal_score(self, calculation_data, _iter_utils=iter_utils, _text_parser=text_parser):
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

      if "author" in bio:
        author_score = -5
        score += author_score
        counter[constants.BIO] += author_score

      if counter[constants.BIO]: internal_score_attrs[constants.BIO] = counter[constants.BIO]

    followers_count = calculation_data[constants.FOLLOWERS_COUNT]
    if followers_count >= 1000:
      followers_count_score = 1
      score += followers_count_score
      internal_score_attrs[constants.FOLLOWERS_COUNT] = followers_count_score

    gender = calculation_data[constants.GENDER]
    if gender:
      if gender == GenderEnum.female:
        female_gender_score = 3
        score += female_gender_score
        internal_score_attrs[constants.GENDER] = female_gender_score

    location = calculation_data[constants.LOCATION]
    if location:
      location_score = 1
      location = location.lower()
      if any(loc in location for loc in self._important_locations):
        score += location_score
        internal_score_attrs[constants.LOCATION] = location_score

    internal_score_attrs[constants.SCORE] = score

    return score, internal_score_attrs

  def get_final_score(self, score_attrs):
    scores = [x['score'] for x in score_attrs]
    return sum(scores)
