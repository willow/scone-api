import requests

from src.libs.nlp_utils.services.enums import GenderEnum
from urllib.request import AbstractBasicAuthHandler


GENDER_API_URL = 'http://api.genderize.io/'


def get_gender(name):
  first_name = name.split(' ')[0]
  params = {"name": first_name}
  gender_response = requests.get(GENDER_API_URL, params=params)
  result = gender_response.json()

  try:
    probability = float(result['probability'])
    comparable_name_count = int(result['count'])

    # comparable_name_count is important because lots of entities have a count of 1 and just seem 'off'
    # ex: "Top" "Bottom" etc. Male, probability is 100% but with a count of 1.
    if probability > .75 and comparable_name_count > 1:
      gender = result['gender'].lower()
      if gender == 'male':
        ret_val = GenderEnum.male
      elif gender == 'female':
        ret_val = GenderEnum.female
      else:
        ret_val = GenderEnum.other
    else:
      ret_val = GenderEnum.unknown
  except:
    ret_val = GenderEnum.unknown

  return ret_val
