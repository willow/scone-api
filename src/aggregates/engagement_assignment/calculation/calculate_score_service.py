from src.aggregates.client.enums import ClientTypeEnum
from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.calculation_data_providers.linkedin_calculation_data_provider \
  import \
  LinkedinCalculationDataProvider
from src.aggregates.engagement_assignment.calculation.calculation_data_providers.reddit_calculation_data_provider \
  import \
  RedditCalculationDataProvider
from src.aggregates.engagement_assignment.calculation.calculation_data_providers.twitter_calculation_data_provider \
  import \
  TwitterCalculationDataProvider
from src.aggregates.engagement_assignment.calculation.rules_engine \
  .appointment_finding_tech_startup_affiliate_rules_engine import \
  AppointmentFindingTechStartupAffiliateRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine \
  .appointment_finding_tech_startup_client_rules_engine import \
  AppointmentFindingTechStartupClientRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.food_lover_tech_startup_rules_engine import \
  FoodLoverTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.marketing_startup_rules_engine import \
  MarketingTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine \
  .professional_social_networking_tech_startup_rules_engine import \
  ProfessionalSocialNetworkingTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.sass_tech_startup_rules_engine import \
  SaaSTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.sports_meetup_tech_startup_rules_engine import \
  SportsMeetupTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.video_convo_tech_startup_rules_engine import \
  VideoConvoTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.ya_author_rules_engine import YAAuthorRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.ya_writing_meetup_rules_engine import \
  YAWritingMeetupRulesEngine
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service
from src.apps.engagement_discovery.enums import ProviderEnum


def calculate_engagement_assignment_score(client, assignment_attrs):
  score_attrs = []
  rules_engine = get_rules_engine(client)

  for assignment_attr, assigned_entity_ids in assignment_attrs.items():

    for assigned_entity_id in assigned_entity_ids:

      if assignment_attr == constants.ASSIGNED_EO_IDS:
        assigned_entity = engagement_opportunity_service.get_engagement_opportunity(assigned_entity_id)
        provider_type = assigned_entity.provider_type
        entity_type = constants.EO
      elif assignment_attr == constants.ASSIGNED_PROFILE_IDS:
        assigned_entity = profile_service.get_profile(assigned_entity_id)
        provider_type = assigned_entity.provider_type
        entity_type = constants.PROFILE
      else:
        raise ValueError("Invalid assignment attrs")

      data_provider = _get_data_provider(provider_type)

      calculation_data = data_provider.provide_calculation_data(client, assigned_entity)

      score, score_components = rules_engine.get_score(calculation_data)

      score_attrs.append({'score': score, 'score_attrs': score_components, 'entity_type': entity_type,
                          'id': assigned_entity_id})

  total_score = rules_engine.get_final_score(score_attrs)

  return total_score, score_attrs


def _get_data_provider(provider_type):
  ret_val = None

  if provider_type == ProviderEnum.twitter:
    ret_val = TwitterCalculationDataProvider()
  elif provider_type == ProviderEnum.reddit:
    ret_val = RedditCalculationDataProvider()
  elif provider_type == ProviderEnum.linkedin:
    ret_val = LinkedinCalculationDataProvider()

  if ret_val:
    return ret_val
  else:
    raise ValueError("Invalid provider type")


def get_rules_engine(client):
  if client.client_type == ClientTypeEnum.saas_tech_startup:
    return SaaSTechStartupRulesEngine()
  elif client.client_type == ClientTypeEnum.marketing_tech_startup:
    return MarketingTechStartupRulesEngine()
  elif client.client_type == ClientTypeEnum.ya_author:
    return YAAuthorRulesEngine()
  elif client.client_type == ClientTypeEnum.video_convo_tech_startup:
    return VideoConvoTechStartupRulesEngine()
  elif client.client_type == ClientTypeEnum.professional_social_networking_tech_startup_rules_engine:
    return ProfessionalSocialNetworkingTechStartupRulesEngine()
  elif client.client_type == ClientTypeEnum.sports_meetup_tech_startup_rules_engine:
    return SportsMeetupTechStartupRulesEngine()
  elif client.client_type == ClientTypeEnum.appointment_finding_tech_startup_affiliate_rules_engine:
    return AppointmentFindingTechStartupAffiliateRulesEngine()
  elif client.client_type == ClientTypeEnum.appointment_finding_tech_startup_client_rules_engine:
    return AppointmentFindingTechStartupClientRulesEngine()
  elif client.client_type == ClientTypeEnum.ya_writing_meetup_rules_engine:
    return YAWritingMeetupRulesEngine()
  elif client.client_type == ClientTypeEnum.food_lover_startup_rules_engine:
    return FoodLoverTechStartupRulesEngine()

  raise ValueError("No rules exist for this client")
