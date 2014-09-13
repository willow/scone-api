import logging
from importlib import import_module

from src.aggregates.client.enums import ClientTypeEnum
from src.apps.engagement_discovery.enums import ProviderChoices


# noinspection PyUnresolvedReferences
# this is how we can do dynamic imports easily
from .client_rules import *

logger = logging.getLogger(__name__)

_provider_choices_dict = dict(ProviderChoices)


def _get_client_rules_module(client_type):
  client_rules_module = import_module("." + client_type, __package__ + '.client_rules')
  return client_rules_module


def get_client_rules_engine_by_type_and_name(client_type, thing_to_score, provider_type=None):
  thing_to_score += "RulesEngine"

  client_type = ClientTypeEnum(client_type).name
  client_rules_module = _get_client_rules_module(client_type)

  provider_name = ''
  if provider_type:
    provider_name = _provider_choices_dict[provider_type]

  class_name = "{0}{1}".format(provider_name, thing_to_score)

  ret_val = getattr(client_rules_module, class_name)

  return ret_val
