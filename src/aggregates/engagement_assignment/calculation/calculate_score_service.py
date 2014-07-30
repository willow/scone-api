from src.aggregates.engagement_assignment import constants

from src.aggregates.client.enums import ClientTypeEnum
from src.aggregates.engagement_assignment.calculation.calculation_objects import CalculationAssignedEntityObject
from src.aggregates.engagement_assignment.calculation.rules_engine \
  .appointment_finding_tech_startup_affiliate_rules_engine import \
  AppointmentFindingTechStartupAffiliateRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine \
  .appointment_finding_tech_startup_client_rules_engine import \
  AppointmentFindingTechStartupClientRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.bitcoin_philippines_startup_rules_engine import \
  BitcoinPhilippinesStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.food_lover_tech_startup_rules_engine import \
  FoodLoverTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.marketing_startup_rules_engine import \
  MarketingTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine \
  .professional_social_networking_tech_startup_rules_engine import \
  ProfessionalSocialNetworkingTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.rules_engine import RulesEngine
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


def calculate_engagement_assignment_score(client, assignment_attrs):
  score_attrs = {}

  assigned_entities = _get_assigned_entities(assignment_attrs)
  prospect = assigned_entities[0].prospect

  rules_engine = RulesEngine(client)

  prospect_score, prospect_score_attrs = rules_engine.get_prospect_score(prospect)
  score_attrs['prospect'] = {
    'score': prospect_score,
    'score_attrs': prospect_score_attrs,
    'id': prospect.id
  }

  # get all unique profiles except those that we're going to assign
  assigned_profiles = [ae.id for ae in assigned_entities if ae.entity_type == constants.PROFILE]
  profiles = prospect.profiles.exclude(id__in=assigned_profiles)

  score_attrs['profiles'] = []
  for profile in profiles:
    profile_score, profile_score_attrs = rules_engine.get_profile_score(profile)
    score_attrs['profiles'].append({
      'score': profile_score,
      'score_attrs': profile_score_attrs,
      'id': profile.id,
      'provider_type': profile.provider_type,
    })

  # loop through ae's
  score_attrs['assigned_entities'] = []
  for ae in assigned_entities:
    ae_score, ae_score_attrs = rules_engine.get_ae_score(ae)
    score_attrs['assigned_entities'].append({
      'score': ae_score,
      'score_attrs': ae_score_attrs,
      'id': ae.id,
      'entity_type': ae.entity_type,
      'provider_type': ae.provider_type
    })

  return score, score_attrs


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
  elif client.client_type == ClientTypeEnum.bitcoin_philippines_startup_rules_engine:
    return BitcoinPhilippinesStartupRulesEngine()

  raise ValueError("No rules exist for this client")


def _get_assigned_entities(assignment_attrs):
  assigned_entities = []
  for assignment_attr, assigned_entity_ids in assignment_attrs.items():

    for assigned_entity_id in assigned_entity_ids:

      if assignment_attr == constants.ASSIGNED_EO_IDS:
        assigned_entity = engagement_opportunity_service.get_engagement_opportunity(assigned_entity_id)
        provider_type = assigned_entity.provider_type
        entity_type = constants.EO
        prospect = assigned_entity.profile.prospect
      elif assignment_attr == constants.ASSIGNED_PROFILE_IDS:
        assigned_entity = profile_service.get_profile(assigned_entity_id)
        provider_type = assigned_entity.provider_type
        entity_type = constants.PROFILE
        prospect = assigned_entity.prospect
      else:
        raise ValueError("Invalid assignment attrs")

      assigned_entities.append(CalculationAssignedEntityObject(assigned_entity, entity_type, provider_type, prospect))

  return assigned_entities
