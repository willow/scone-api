from unittest.mock import MagicMock

from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation import score_processor, score_data_provider
from src.aggregates.engagement_assignment.tests.ea_test_data import assignment_1, client_1, client_1_score_data


def _get_score_data_provider():
  score_data_provider_mock = MagicMock(spec=score_data_provider)
  score_data_provider_mock.client_score_provider_bounds.return_value = client_1_score_data
  return score_data_provider_mock


def test_score_processor_returns_correct_total_for_ae_attrs():
  score_data_provider_mock = _get_score_data_provider()
  _, ret_val = score_processor.process_score(client_1, assignment_1, score_data_provider_mock)

  assert ret_val[constants.ASSIGNED_ENTITIES][0][constants.SCORE] == .3

def test_score_processor_returns_correct_total_for_profile_attrs():
  score_data_provider_mock = _get_score_data_provider()
  _, ret_val = score_processor.process_score(client_1, assignment_1, score_data_provider_mock)

  assert ret_val[constants.PROFILES][0][constants.SCORE] == .5

def test_score_processor_returns_correct_total_for_prospect_attrs():
  score_data_provider_mock = _get_score_data_provider()
  _, ret_val = score_processor.process_score(client_1, assignment_1, score_data_provider_mock)

  assert ret_val[constants.PROSPECT][constants.SCORE] == .125
