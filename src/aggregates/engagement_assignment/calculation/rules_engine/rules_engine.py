import logging

from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.rules_engine import rules_engine_class_provider
from src.apps.engagement_discovery.enums import ProviderChoices


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

  def get_assigned_entity_score(self, assigned_entity_object, calc_data):
    rules_class = self._get_client_rules_engine_by_type_and_name(
      _assigned_entity_names[assigned_entity_object.entity_type], assigned_entity_object.provider_type
    )

    rules_instance = rules_class(assigned_entity_object.assigned_entity, calc_data)

    return rules_instance.score_it()

  def _get_client_rules_engine_by_type_and_name(self, thing_to_score, provider_type=None):
    rules_class = rules_engine_class_provider.get_client_rules_engine_by_type_and_name(
      self.client.client_type, thing_to_score, provider_type
    )

    return rules_class
