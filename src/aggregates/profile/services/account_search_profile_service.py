from src.apps.engagement_discovery.enums import ProviderEnum
from src.aggregates.profile import constants


def get_social_account_info_from_profile(profile):
  if profile.provider_type == ProviderEnum.linkedin:
    social_account_uid = profile.profile_attrs[constants.LINKEDIN_VIEW_ID]
  elif profile.provider_type == ProviderEnum.twitter:
    social_account_uid = profile.profile_external_id
  else:
    raise ValueError("invalid provider type")

  return ProviderEnum(profile.provider_type).name, social_account_uid


def is_valid_profile_for_account_search(profile):
  ret_val = False

  provider = profile.provider_type
  if provider in (ProviderEnum.twitter,):
    ret_val = True

  return ret_val
