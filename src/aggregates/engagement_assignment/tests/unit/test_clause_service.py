import random
from unittest.mock import MagicMock
from src.aggregates.engagement_assignment.recommendation import clause_service
from src.apps.engagement_discovery.enums import ProviderEnum


def test_tweet_options_exist_for_ta_action_clause():
  # Arrange
  mock_recommendation_data = {}
  mock_recommendation_data['contains_link'] = False
  mock_recommendation_data['provider_type'] = ProviderEnum.twitter
  mock_randomizer = MagicMock(spec=random)

  # Act
  clause_service.get_ta_action_clause(mock_recommendation_data, mock_randomizer)

  # Assert
  assert 'just tweeted about' in mock_randomizer.choice.call_args[0][0]
