from src.aggregates.client.enums import ClientTypeEnum
from src.aggregates.engagement_assignment.calculation.calculation_data_providers.reddit_calculation_data_provider \
  import \
  RedditCalculationDataProvider
from src.aggregates.engagement_assignment.calculation.calculation_data_providers.twitter_calculation_data_provider \
  import \
  TwitterCalculationDataProvider
from src.aggregates.engagement_assignment.calculation.rules_engine.tech_startup_rules_engine import \
  TechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.ya_author_rules_engine import YAAuthorRulesEngine
from src.apps.engagement_discovery.enums import ProviderEnum


def calculate_engagement_assignment_score(client, engagement_opportunity):
  data_provider = _get_data_provider(engagement_opportunity)

  calculation_data = data_provider.provide_calculation_data(client, engagement_opportunity)

  rules_engine = get_rules_engine(client)

  score, score_attrs = rules_engine.get_score(calculation_data)

  return score, score_attrs


def _get_data_provider(engagement_opportunity):
  if engagement_opportunity.provider_type == ProviderEnum.twitter:
  # we know that all eo's will be tweets (for now), so just use twitter calc data service.
    return TwitterCalculationDataProvider()
  elif engagement_opportunity.provider_type == ProviderEnum.reddit:
    return RedditCalculationDataProvider()
    
  raise ValueError("Invalid provider type")

def get_rules_engine(client):
  if client.client_type == ClientTypeEnum.tech_startup:
    return TechStartupRulesEngine()
  elif client.client_type == ClientTypeEnum.ya_author:
    return YAAuthorRulesEngine()

  raise ValueError("No rules exist for this client")
