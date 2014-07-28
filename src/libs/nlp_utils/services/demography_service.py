from django.conf import settings
import requests

from src.libs.nlp_utils.services.enums import GenderEnum


GENDER_API_URL = 'https://genderize.p.mashape.com/'
MASHAPE_API_KEY = settings.MASHAPE_API_KEY


def get_gender(name):
  first_name = name.split(' ')[0]

  params = {
    "name": first_name,
  }

  headers = {
    "X-Mashape-Authorization": MASHAPE_API_KEY
  }

  gender_response = requests.get(GENDER_API_URL, params=params, headers=headers)

  try:
    gender_response.raise_for_status()
  except Exception as e:
    raise OSError("Error making request to genderize. params: %s", params) from e

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
