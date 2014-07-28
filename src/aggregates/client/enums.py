from enum import IntEnum


class ClientTypeEnum(IntEnum):
  saas_tech_startup = 1
  marketing_tech_startup = 2
  ya_author = 3
  video_convo_tech_startup = 4
  professional_social_networking_tech_startup_rules_engine = 5
  appointment_finding_tech_startup_affiliate_rules_engine = 6
  appointment_finding_tech_startup_client_rules_engine = 7
  sports_meetup_tech_startup_rules_engine = 8
  ya_writing_meetup_rules_engine = 9
  food_lover_startup_rules_engine = 10


ClientTypeChoices = (
  (ClientTypeEnum.saas_tech_startup.value, 'tech startup (sass)'),
  (ClientTypeEnum.marketing_tech_startup.value, 'tech startup (marketing)'),
  (ClientTypeEnum.ya_author.value, 'young adult author'),
  (ClientTypeEnum.video_convo_tech_startup.value, 'tech startup (video convo)'),
  (ClientTypeEnum.professional_social_networking_tech_startup_rules_engine.value, 'tech startup (professional social '
                                                                                  'networking)'),
  (ClientTypeEnum.appointment_finding_tech_startup_affiliate_rules_engine.value, 'tech startup(appointment finding '
                                                                                 'affiliate)'),
  (ClientTypeEnum.appointment_finding_tech_startup_client_rules_engine.value, 'tech startup(appointment finding '
                                                                              'client)'),
  (ClientTypeEnum.sports_meetup_tech_startup_rules_engine.value, 'tech startup (sports meetup)'),
  (ClientTypeEnum.ya_writing_meetup_rules_engine.value, 'ya writing meetup'),
  (ClientTypeEnum.food_lover_startup_rules_engine.value, 'tech startup (food lovers)'),
)
