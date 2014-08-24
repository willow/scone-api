import logging
from src.aggregates.client.enums import ClientTypeEnum
from importlib import import_module
from src.aggregates.engagement_assignment import constants
from src.apps.engagement_discovery.enums import ProviderChoices

# noinspection PyUnresolvedReferences
# this is how we can do dynamic imports easily
from .client_rules import *

logger = logging.getLogger(__name__)

_provider_choices_dict = dict(ProviderChoices)

_assigned_entity_names = {
  constants.EO: "EngagementOpportunity",
  constants.PROFILE: "Profile",
}


class RulesEngine():
  def __init__(self, client):
    self.client = client

  def get_prospect_score(self, prospect, calc_data):
    rules_class = self._get_client_rules_engine_by_type_and_name('Prospect')

    rules_instance = rules_class(prospect, calc_data)

    return rules_instance.score_it()

  def get_profile_score(self, profile, calc_data):
    rules_class = self._get_client_rules_engine_by_type_and_name('Profile', profile.provider_type)

    rules_instance = rules_class(profile, calc_data)

    return rules_instance.score_it()

  def get_assigned_entity_score(self, assigned_entity_object):
    rules_class = self._get_client_rules_engine_by_type_and_name(
      _assigned_entity_names[assigned_entity_object.entity_type], assigned_entity_object.provider_type
    )()

    return rules_class.score_it(assigned_entity_object)

  def _get_client_rules_engine_by_type_and_name(self, thing_to_score, provider_type=None):
    thing_to_score += "RulesEngine"

    client_type = ClientTypeEnum(self.client.client_type).name
    client_rules_module = import_module("." + client_type, __package__ + '.client_rules')

    provider_name = ''
    if provider_type:
      provider_name = _provider_choices_dict[provider_type]

    class_name = "{0}{1}".format(provider_name, thing_to_score)

    ret_val = getattr(client_rules_module, class_name)

    return ret_val
