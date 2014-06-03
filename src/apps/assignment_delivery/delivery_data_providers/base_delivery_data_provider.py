from abc import ABC


class BaseDeliveryDataProvider(ABC):
  def provide_delivery_data(self, engagement_assignment):
    ret_val = {}
    engagement_opportunity = engagement_assignment.engagement_opportunity
    ret_val["provider_type"] = engagement_opportunity.provider_type

    return ret_val
