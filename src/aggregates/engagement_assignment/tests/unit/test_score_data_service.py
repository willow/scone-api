import pytest
import numpy as np
from unittest.mock import MagicMock

from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation import score_data_service, score_data_repository
from src.aggregates.engagement_assignment.tests.ea_test_data import client_1, \
  client_1_scores
from src.libs.numpy_utils import array_utils


def _get_score_data_repo():
  score_data_repo_mock = MagicMock(spec=score_data_repository)
  data = client_1_scores
  score_data_repo_mock.get_recent_client_scores.return_value = data
  return score_data_repo_mock


def _get_array_utils():
  array_utils_mock = MagicMock(spec=array_utils)
  array_utils_mock.filter_by_median_absolute_deviation.return_value = np.array([10.])
  return array_utils_mock


# region test bounds
def test_score_data_service_assigns_correct_prospect_upper_bound_score():
  score_data_repo_mock = _get_score_data_repo()
  array_utils_mock = _get_array_utils()
  _, ret_val = score_data_service.set_client_bounds_score(client_1, score_data_repo_mock, array_utils_mock)
  assert round(ret_val[constants.PROSPECT][constants.SCORE], 3) == 0.214

# endregion test bounds
