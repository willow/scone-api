from src.apps.engagement_discovery.enums import ProviderEnum


def _get_client_score_provider_bounds(client):
  return {ProviderEnum.reddit:0}

def get_client_score_data(client):
  return _get_client_score_provider_bounds(client)

