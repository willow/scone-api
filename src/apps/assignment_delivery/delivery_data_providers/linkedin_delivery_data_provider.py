from src.aggregates.profile.models import Profile
from src.apps.assignment_delivery import constants
from src.apps.assignment_delivery.delivery_data_providers.base_delivery_data_provider import BaseDeliveryDataProvider


class LinkedinDeliveryDataProvider(BaseDeliveryDataProvider):
  def _provide_internal_delivery_data(self, assigned_entity):
    if not isinstance(assigned_entity, Profile):
      raise ValueError("This data provider only works with Profiles's")
    else:
      profile = assigned_entity

    ret_val = {}

    profile_attrs = profile.profile_attrs

    ret_val[constants.USERNAME] = profile_attrs.get(constants.PROFILE_URL)
    ret_val[constants.NAME] = profile_attrs.get(constants.NAME)
    ret_val[constants.FOLLOWERS_COUNT] = None
    ret_val[constants.FOLLOWING_COUNT] = profile_attrs.get(constants.NUMBER_OF_CONNECTIONS)
    ret_val[constants.URL] = profile_attrs[constants.PROFILE_URL]
    ret_val[constants.BIO] = profile_attrs.get(constants.TEXT)

    return ret_val


