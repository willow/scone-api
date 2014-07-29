from src.aggregates.client.enums import ClientTypeEnum
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
from src.aggregates.engagement_assignment.calculation.rules_engine.sass_tech_startup_rules_engine import \
  SaaSTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.sports_meetup_tech_startup_rules_engine import \
  SportsMeetupTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.video_convo_tech_startup_rules_engine import \
  VideoConvoTechStartupRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.ya_author_rules_engine import YAAuthorRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.ya_writing_meetup_rules_engine import \
  YAWritingMeetupRulesEngine


def calculate_engagement_assignment_score(client, assignment_attrs):
  rules_engine = get_rules_engine(client)

  score, score_attrs = rules_engine.get_score(assignment_attrs)

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
