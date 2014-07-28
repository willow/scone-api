import random
from src.aggregates.engagement_assignment import constants

from src.apps.engagement_discovery.enums import ProviderEnum
from src.libs.nlp_utils.services import keyword_service
from src.libs.text_utils.parsers import text_parser


BASE_TA_ACTION_CLAUSES = ('just shared their thoughts on', 'recently posted a message about', 'is talking about')

BASE_RESPONSE_CLAUSES = (
  'Consider telling {name} your thoughts.', 'Let them know your thoughts.', 'What do you think?',
  'Perhaps you could share your impression.'
)


def get_ta_action_clause(recommendation_data, _randomizer=random):
  action_clauses = BASE_TA_ACTION_CLAUSES

  provider_type = recommendation_data[constants.PROVIDER_TYPE]

  contains_links = recommendation_data[constants.CONTAINS_LINK]

  if contains_links:
    action_clauses = action_clauses + ('just shared a link about', 'is linking to a site about')

  if provider_type == ProviderEnum.twitter:
    action_clauses = action_clauses + ('just tweeted about', 'posted a tweet for')

    if contains_links:
      action_clauses = action_clauses + ('just tweeted a link about', 'shared a link in a tweet about')

  return _randomizer.choice(action_clauses)


def get_ta_name_clause(recommendation_data):
  ta_name = recommendation_data[constants.NAME]

  return ta_name


def get_about_clause(recommendation_data):
  return recommendation_data[constants.TEXT][:25] + "..."


def get_response_clause(recommendation_data, _randomizer=random):
  response_clause = _randomizer.choice(BASE_RESPONSE_CLAUSES)

  return response_clause.format(name=recommendation_data[constants.NAME])
