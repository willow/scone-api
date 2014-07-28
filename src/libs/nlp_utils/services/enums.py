from enum import IntEnum


class NamedEntityTypeEnum(IntEnum):
  any = 0
  person = 1
  other = 99
  unknown = 100


class GenderEnum(IntEnum):
  male = 1
  female = 2
  other = 3
  unknown = 100
