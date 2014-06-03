from src.libs.nlp_utils.services import demography_service

from src.libs.nlp_utils.services.enums import NamedEntityTypeEnum, GenderEnum


def get_entity_type(entity_name, _demography_service=demography_service):
  # temporarily use gender service to get entity type so we don't hit alchemy api limit
  gender = _demography_service.get_gender(entity_name)
  if gender == GenderEnum.unknown:
    ret_val = NamedEntityTypeEnum.unknown
  else:
    ret_val = NamedEntityTypeEnum.person

  return ret_val
