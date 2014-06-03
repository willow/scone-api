from enum import IntEnum


class ClientTypeEnum(IntEnum):
  tech_startup = 1
  ya_author = 2
  
ClientTypeChoices = (
  (ClientTypeEnum.tech_startup.value, 'tech startup'),
  (ClientTypeEnum.ya_author.value, 'young adult author'),
)
