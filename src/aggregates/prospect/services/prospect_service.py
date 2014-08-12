import logging

from src.aggregates.profile.services import account_search_profile_service
from src.aggregates.profile.services.account_search_profile_service import is_valid_profile_for_account_search
from src.aggregates.prospect import constants
from src.aggregates.profile.models import Profile
from src.aggregates.prospect import factories
from src.aggregates.prospect.models import Prospect
from src.aggregates.prospect.services import account_search_prospect_service
from src.libs.python_utils.logging.logging_utils import log_wrapper
from src.libs.social_utils.account_search.services.account_search_service import get_social_account_data


logger = logging.getLogger(__name__)


def save_or_update(prospect):
  prospect.save(internal=True)


def get_prospect(prospect_id):
  return Prospect.objects.get(pk=prospect_id)


def get_prospect_from_uid(prospect_uid):
  return Prospect.objects.get(prospect_uid=prospect_uid)


def save_prospect_from_provider_info(profile_external_id, provider_type):
  from src.aggregates.profile.services.profile_service import get_profile_from_provider_info

  try:
    profile = get_profile_from_provider_info(
      profile_external_id,
      provider_type
    )

    ret_val = profile.prospect
  except Profile.DoesNotExist:
    # we could get initial prospect info from a 3rd party api. We could get email addresses, etc.
    prospect_attrs = {}
    ret_val = factories.construct_prospect_from_attrs(prospect_attrs)
    save_or_update(ret_val)

  return ret_val


def manage_prospect_profiles(prospect):
  profiles = prospect.profiles.all()

  if profiles.count() == 1:
    profile = profiles.get()

    if is_valid_profile_for_account_search(profile):
      try:
        provider_name, account_uid = account_search_profile_service.get_social_account_info_from_profile(profile)
      except:
        pass

      else:

        log_message = (
          "Get social account data. provider_name: %s, account_uid: %s",
          provider_name, account_uid
        )

        try:
          with log_wrapper(logger.debug, *log_message):
            data = get_social_account_data(provider_name, account_uid)

        except:
          logger.exception("Error: " + log_message[0], *log_message[1:])

        else:
          prospect_attrs = {}

          if data.organizations:
            prospect_attrs[constants.ORGANIZATIONS] = data.organizations

          if data.relative_dob:
            prospect_attrs[constants.RELATIVE_DOB] = data.relative_dob

          if data.gender:
            prospect_attrs[constants.GENDER] = data.gender

          if data.topics:
            prospect_attrs[constants.TOPICS] = data.topics

          if prospect_attrs:
            prospect.update_attrs(prospect_attrs)
            save_or_update(prospect)

          account_search_prospect_service.populate_prospect_child_profile_from_account_search(prospect, data)

  return prospect


def manage_prospect_attrs(prospect, profile):
  profile_location = profile.profile_attrs.get(constants.LOCATION)

  if profile_location:
    prospect.update_attrs({constants.LOCATION: profile_location})

  save_or_update(prospect)
  return prospect
