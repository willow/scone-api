from dateutil import relativedelta
from django.conf import settings
from django.utils import timezone
import requests
from src.libs.python_utils.collections import iter_utils
from src.libs.social_utils.account_search.account_search_result_object import AccountSearchResultObject

api_key = settings.FULLCONTACT_API_KEY
api_endpoint = "https://api.fullcontact.com/v2/person.json"

# reuse a session will use persistent connections
client = requests.Session()


def get_social_account_data(social_network_name, social_account_uid, _iter_utils=iter_utils):
  params = {"apiKey": api_key, "style": "dictionary", social_network_name: social_account_uid}
  resp = client.get(api_endpoint, params=params, timeout=settings.HTTP_TIMEOUT)
  resp.raise_for_status()

  result = resp.json()

  profs = result["socialProfiles"]

  twitter_url = profs.get('twitter')

  if twitter_url:
    twitter_url = twitter_url[0]['url']

  linkedin_url = profs.get('linkedin')

  if linkedin_url:
    linkedin_url = linkedin_url[0]['url']

  demographics = result["demographics"]

  relative_dob = demographics.get('age')
  if relative_dob:
    relative_dob = int(relative_dob)
    relative_dob = timezone.now() - relativedelta.relativedelta(years=relative_dob)

  gender = demographics.get('gender')
  if gender: gender = gender.lower()

  organizations = result.get("organizations")
  if organizations:
    organizations = [
      {
        "name": x['name'],
        "title": x['title'],
        "start_date": x['startDate'],
        "is_primary": x['isPrimary'],
      } for x in organizations
    ]

  topics = None
  footprint = result.get('digitalFootprint')
  if footprint:
    topics = footprint.get('topics')
    if topics:
      klout_topics = topics.get('klout')
      topics = [
        {
          "topic_name": x['value'],
          "snowball_stem": _iter_utils.stemmify_string(x['value'])
        } for x in klout_topics
      ]

  ret_val = AccountSearchResultObject(twitter_url, linkedin_url, organizations, relative_dob, gender, topics)

  return ret_val
