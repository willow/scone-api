from unittest.mock import MagicMock

from src.aggregates.engagement_assignment.recommendation import clause_service

from src.aggregates.engagement_assignment.recommendation.recommendation_builder import RecommendationBuilder
from src.aggregates.engagement_opportunity.models import EngagementOpportunity


def test_target_action_verb_identified():
  mock_clause_service = MagicMock(spec=clause_service)
  mock_clause_service.get_ta_action_clause.return_value = 'just shared'
  mock_engagement_opportunity = MagicMock(spec=EngagementOpportunity)
  builder = RecommendationBuilder(mock_engagement_opportunity, mock_clause_service)

  builder._set_ta_action_clause()

  assert builder._target_action_clause == "just shared"

def test_name_identified():
  mock_clause_service = MagicMock(spec=clause_service)
  mock_clause_service.get_ta_name_clause.return_value = 'NAME'
  mock_engagement_opportunity = MagicMock(spec=EngagementOpportunity)  
  builder = RecommendationBuilder(mock_engagement_opportunity, mock_clause_service)
  
  builder._set_ta_name_clause()
  
  assert builder._ta_name_clause == 'NAME'
