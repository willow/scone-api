from src.aggregates.profile.models import Profile


def construct_profile_from_provider_info_and_profile_attrs(profile_external_id, provider_type, profile_attrs):
  profile = Profile._from_provider_info_and_profile_attrs(profile_external_id, provider_type, profile_attrs)
  return profile
