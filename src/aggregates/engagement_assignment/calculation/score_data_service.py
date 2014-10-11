from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation import score_data_repository
from src.apps.engagement_discovery.enums import ProviderEnum
import numpy as np
from src.libs.numpy_utils import array_utils


def _get_client_score_bounds(client):
  return {ProviderEnum.reddit: 0}


def get_client_score_data(client):
  return _get_client_score_bounds(client)


def _get_highest_score(scores_list, _array_utils):
  scores_array = np.array(scores_list)
  highest_prospect_score = float(_array_utils.filter_by_median_absolute_deviation(scores_array).max())
  return highest_prospect_score


def set_client_bounds_score(client, _score_data_repository=None, _array_utils=None):
  if not _score_data_repository: _score_data_repository = score_data_repository
  if not _array_utils: _array_utils = array_utils

  ret_val = {}
  recent_scores = score_data_repository.get_recent_client_scores(client)

  prospect_scores = recent_scores.pop(constants.PROSPECT_RECENT_SCORES)
  highest_prospect_score = _get_highest_score(prospect_scores, _array_utils)
  ret_val[constants.PROSPECT_UPPER_BOUND_SCORE] = highest_prospect_score

  _score_data_repository.save_client_prospect_bounds_score(client, highest_prospect_score)
