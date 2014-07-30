import pytest
from src.aggregates.client.enums import ClientTypeEnum
from src.aggregates.engagement_assignment.tests.ea_test_data import ClientFactory, EngagementOpportunityFactory
from src.apps.engagement_discovery.enums import ProviderEnum, ProviderActionEnum


@pytest.mark.django_db()
def test_saas_rules_engine_score():
  client = ClientFactory.create(client_type=ClientTypeEnum.saas_tech_startup)

  eo = EngagementOpportunityFactory.create(
    provider_type=ProviderEnum.twitter,
    provider_action_type=ProviderActionEnum.twitter_tweet
  )
