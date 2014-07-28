from abc import ABC, abstractmethod
from src.aggregates.engagement_opportunity.models import EngagementOpportunity
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.models import Profile
from src.aggregates.profile.services import profile_service
from src.apps.assignment_delivery import constants


class BaseDeliveryDataProvider(ABC):
  def _provide_base_delivery_data(self, assigned_entity):
    ret_val = {}

    provider_type = getattr(assigned_entity, 'provider_type')

    if provider_type:
      ret_val["provider_type"] = provider_type

    if isinstance(assigned_entity, EngagementOpportunity):
      assigned_entity = engagement_opportunity_service.get_engagement_opportunity(assigned_entity.id)
      prospect = assigned_entity.profile.prospect
    elif isinstance(assigned_entity, Profile):
      assigned_entity = profile_service.get_profile(assigned_entity.id)
      prospect = assigned_entity.prospect
    else:
      raise ValueError("Invalid assignment attrs")

    attrs = prospect.prospect_attrs or {}
    emails = attrs.get(constants.EMAIL_ADDRESSES)
    ret_val[constants.EMAIL_ADDRESSES] = emails

    return ret_val


  def provide_delivery_data(self, assigned_entity):
    ret_val = self._provide_internal_delivery_data(assigned_entity)

    base_data = self._provide_base_delivery_data(assigned_entity)

    ret_val.update(base_data)

    return ret_val


  @abstractmethod
  def _provide_internal_delivery_data(self, assigned_entity):
    """Get the client-specific rules"""
