from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation import score_data_service


def _get_upper_bound_key(entity_type):
  return entity_type + '_upper_bound_score'


def _get_provider_upper_bound_score(entity_type, entity_attrs, score_data):
  provider_type = entity_attrs.get(constants.PROVIDER_TYPE)

  if provider_type:
    provider_data = score_data[provider_type]
  else:
    # some entities (like prospects) are not provider-specific
    provider_data = score_data

  upper_bound_key = _get_upper_bound_key(entity_type)

  ret_val = provider_data[upper_bound_key]

  return ret_val


def _process_assigned_entities(score_attrs, score_data):
  assigned_entities = score_attrs[constants.ASSIGNED_ENTITIES]

  for ae_attrs in assigned_entities:
    score = ae_attrs[constants.BASE_SCORE] + ae_attrs[constants.INTERNAL_SCORE]
    provider_upper_bound_score = _get_provider_upper_bound_score(ae_attrs[constants.ENTITY_TYPE], ae_attrs, score_data)
    ae_attrs[constants.SCORE] = score / provider_upper_bound_score


def _process_profiles(score_attrs, score_data):
  profiles = score_attrs[constants.PROFILES]

  for profile_attrs in profiles:
    score = profile_attrs[constants.BASE_SCORE] + profile_attrs[constants.INTERNAL_SCORE]
    provider_upper_bound_score = _get_provider_upper_bound_score(constants.PROFILE, profile_attrs, score_data)
    profile_attrs[constants.SCORE] = score / provider_upper_bound_score


def _process_prospect(score_attrs, score_data):
  prospect_attrs = score_attrs[constants.PROSPECT]

  score = prospect_attrs[constants.BASE_SCORE] + prospect_attrs[constants.INTERNAL_SCORE]
  provider_upper_bound_score = _get_provider_upper_bound_score(constants.PROSPECT, prospect_attrs, score_data)
  profile_score = score_attrs[constants.PROFILES][0][constants.SCORE]
  prospect_attrs[constants.SCORE] = score * profile_score / provider_upper_bound_score


def process_score(client, score_attrs, _score_data_service=None):
  if not _score_data_service: _score_data_service = score_data_service

  score_data = _score_data_service.get_client_score_provider_bounds(client)

  _process_assigned_entities(score_attrs, score_data)
  _process_profiles(score_attrs, score_data)
  _process_prospect(score_attrs, score_data)

  return 0, score_attrs
