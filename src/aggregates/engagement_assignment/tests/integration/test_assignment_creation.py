import pytest
from src.aggregates.client.enums import ClientTypeEnum
from src.aggregates.engagement_assignment.tests.ea_test_data import ClientFactory


@pytest.mark.django_db()
def test_saas_rules_engine_score():
  assert ClientFactory.create(
    client_type=ClientTypeEnum.saas_tech_startup
  )
