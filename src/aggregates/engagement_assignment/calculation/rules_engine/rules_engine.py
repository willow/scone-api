import logging
from src.aggregates.client.enums import ClientTypeEnum
from importlib import import_module
from src.apps.engagement_discovery.enums import ProviderEnum


logger = logging.getLogger(__name__)


class RulesEngine():
  def __init__(self, client):
    self.client = client

  def get_prospect_score(self, prospect):
    rules_class = self._get_client_rules_engine_by_type_and_name('Prospect')()
    return rules_class.score_it(prospect)

  def get_profile_score(self, profile):
    pass

  def get_assigned_entity_score(self, assigned_entity_object):
    pass

  def _get_client_rules_engine_by_type_and_name(self, thing_to_score, provider_type=None):
    client_type = ClientTypeEnum(self.client.client_type)
    client_rules_module = import_module(client_type, '.client_rules')

    provider_name = None
    if provider_type:
      provider_name = ProviderEnum(provider_type)
      provider_name = provider_name[0].upper() + provider_name[1:]

    class_name = "{provider_name}{thing_to_score}".format(provider_name, thing_to_score)

    ret_val = getattr(client_rules_module, class_name)

    return ret_val
