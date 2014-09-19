from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation import score_data_provider


def _get_upper_bound_key(entity_type):
  return entity_type + '_upper_bound_score'


def _process_assigned_entities(score_attrs, score_data):
  ae_attrs = score_attrs[constants.ASSIGNED_ENTITIES]
  for ae_attr in ae_attrs:
    score = ae_attr[constants.BASE_SCORE]
    provider_data = score_data[ae_attr[constants.PROVIDER_TYPE]]
    upper_bound_key = _get_upper_bound_key(ae_attr[constants.ENTITY_TYPE])
    provider_upper_bound_score = provider_data[upper_bound_key]
    ae_attr[constants.BASE_SCORE] = score / provider_upper_bound_score


def process_score(client, score_attrs, _score_data_provider=None):
  if not _score_data_provider: _score_data_provider = score_data_provider

  score_data = _score_data_provider.client_score_provider_bounds(client)

  _process_assigned_entities(score_attrs, score_data)

  return 0, score_attrs
