from src.aggregates.engagement_assignment import constants

from src.aggregates.client.enums import ClientTypeEnum
from src.aggregates.engagement_assignment.calculation import calculate_data_service
from src.aggregates.engagement_assignment.calculation.calculation_objects import CalculationAssignedEntityObject
from src.aggregates.engagement_assignment.calculation.rules_engine.rules_engine import RulesEngine
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service


def _get_calc_data(assigned_calc_objects, client, _calc_data_service=None):
  if not _calc_data_service: _calc_data_service = calculate_data_service
  ret_val = {}

  stemmed_keywords = _calc_data_service.provide_stemmed_keywords(client, assigned_calc_objects)
  ret_val[constants.STEMMED_TA_TOPIC_KEYWORDS] = stemmed_keywords

  client_uid = _calc_data_service.provide_client_uid(client)
  ret_val[constants.CLIENT_UID] = client_uid

  return ret_val


def calculate_engagement_assignment_score(client, assignment_attrs):
  score_attrs = {}

  assigned_calc_objects = _get_assigned_calc_objects(assignment_attrs)
  prospect = assigned_calc_objects[0].prospect

  calc_data = _get_calc_data(assigned_calc_objects, client)

  rules_engine = RulesEngine(client)

  prospect_score_object = rules_engine.get_prospect_score(prospect, calc_data)
  score_attrs['prospect'] = {
    'base_score': prospect_score_object.base_score,
    'base_score_attrs': prospect_score_object.base_score_attrs,
    'internal_score': prospect_score_object.internal_score,
    'internal_score_attrs': prospect_score_object.internal_score_attrs,
    'id': prospect.id
  }

  # get all unique profiles except those that we're going to assign
  assigned_profiles = [ae.id for ae in assigned_calc_objects if ae.entity_type == constants.PROFILE]
  profiles = prospect.profiles.exclude(id__in=assigned_profiles)

  score_attrs['profiles'] = []
  for profile in profiles:
    profile_score_object = rules_engine.get_profile_score(profile)
    score_attrs['profiles'].append({
      'base_score': profile_score_object.base_score,
      'base_score_attrs': profile_score_object.base_score_attrs,
      'internal_score': profile_score_object.internal_score,
      'internal_score_attrs': profile_score_object.internal_score_attrs,
      'id': profile.id,
      'provider_type': profile.provider_type,
    })

  # loop through ae's
  score_attrs['assigned_entities'] = []
  for ae in assigned_calc_objects:
    ae_score_object = rules_engine.get_assigned_entity_score(ae)
    score_attrs['assigned_entities'].append({
      'base_score': ae_score_object.base_score,
      'base_score_attrs': ae_score_object.base_score_attrs,
      'internal_score': ae_score_object.internal_score,
      'internal_score_attrs': ae_score_object.internal_score_attrs,
      'id': ae.assigned_entity_id,
      'entity_type': ae.entity_type,
      'provider_type': ae.provider_type
    })

  return 0, score_attrs


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


def _get_assigned_calc_objects(assignment_attrs):
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

      assigned_entities.append(
        CalculationAssignedEntityObject(assigned_entity, assigned_entity.id, entity_type, provider_type, prospect)
      )

  return assigned_entities
