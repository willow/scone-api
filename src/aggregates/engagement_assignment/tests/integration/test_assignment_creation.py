import pytest
from unittest.mock import patch

from src.aggregates.client.enums import ClientTypeEnum
from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation import calculate_score_service
from src.aggregates.engagement_assignment.tests import test_client_rules_engine
from src.aggregates.engagement_assignment.tests.ea_test_data import ClientFactory, EngagementOpportunityFactory, \
  EngagementAssignmentFactory
from src.apps.engagement_discovery.enums import ProviderEnum, ProviderActionEnum


@pytest.mark.django_db()
def test_saas_rules_engine_score():
  client = ClientFactory.create(client_type=ClientTypeEnum.saas_tech_startup)

  eo = EngagementOpportunityFactory.create(
    provider_type=ProviderEnum.twitter,
    provider_action_type=ProviderActionEnum.twitter_tweet,
  )

  ea = EngagementAssignmentFactory.build(assignment_attrs={constants.ASSIGNED_EO_IDS: [eo.id]})

  calculate_score_service.calculate_engagement_assignment_score(client, ea.assignment_attrs)


rules_engine_provider = 'src.aggregates.engagement_assignment.calculation.rules_engine.rules_engine_class_provider' \
                        '._get_client_rules_module'


@pytest.mark.django_db()
@patch(rules_engine_provider)
def test_prospect_score_from_test_client_rules_engine(class_provider_mock):
  class_provider_mock.return_value = test_client_rules_engine

  client = ClientFactory.create(client_type=ClientTypeEnum.saas_tech_startup)

  eo = EngagementOpportunityFactory.create(
    provider_type=ProviderEnum.twitter,
    provider_action_type=ProviderActionEnum.twitter_tweet,
  )

  ea = EngagementAssignmentFactory.build(assignment_attrs={constants.ASSIGNED_EO_IDS: [eo.id]})

  calculate_score_service.calculate_engagement_assignment_score(client, ea.assignment_attrs)
