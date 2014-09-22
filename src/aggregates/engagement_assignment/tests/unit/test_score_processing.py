from unittest.mock import MagicMock

from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation import score_processor, score_data_service
from src.aggregates.engagement_assignment.tests.ea_test_data import assignment_1, client_1, client_1_score_provider_data, \
  assignment_2


def _get_score_data_service():
  score_data_service_mock = MagicMock(spec=score_data_service)
  score_data_service_mock.client_score_provider_bounds.return_value = client_1_score_provider_data
  return score_data_service_mock


# region test different providers
def test_score_processor_returns_correct_total_for_assignment_1_ae_attrs():
  score_data_service_mock = _get_score_data_service()
  _, ret_val = score_processor.process_score(client_1, assignment_1, score_data_service_mock)

  assert ret_val[constants.ASSIGNED_ENTITIES][0][constants.SCORE] == .3


def test_score_processor_returns_correct_total_for_assignment_1_profile_attrs():
  score_data_service_mock = _get_score_data_service()
  _, ret_val = score_processor.process_score(client_1, assignment_1, score_data_service_mock)

  assert ret_val[constants.PROFILES][0][constants.SCORE] == .5


def test_score_processor_returns_correct_total_for_assignment_1_prospect_attrs():
  score_data_service_mock = _get_score_data_service()
  _, ret_val = score_processor.process_score(client_1, assignment_1, score_data_service_mock)

  assert ret_val[constants.PROSPECT][constants.SCORE] == .125


def test_score_processor_returns_correct_total_for_assignment_2_ae_attrs():
  score_data_service_mock = _get_score_data_service()
  _, ret_val = score_processor.process_score(client_1, assignment_2, score_data_service_mock)

  assert ret_val[constants.ASSIGNED_ENTITIES][0][constants.SCORE] == .5


def test_score_processor_returns_correct_total_for_assignment_2_profile_attrs():
  score_data_service_mock = _get_score_data_service()
  _, ret_val = score_processor.process_score(client_1, assignment_2, score_data_service_mock)

  assert ret_val[constants.PROFILES][0][constants.SCORE] == .5

# endregion test different providers
