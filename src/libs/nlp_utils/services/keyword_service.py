import requests
from django.conf import settings

ALCHEMY_KEYWORD_PROCESS_URL = 'http://access.alchemyapi.com/calls/text/TextGetRankedKeywords'
_alchemy_key = settings.ALCHEMY_API_KEY


def get_keywords(text):
  """
    Returns a a list of keywords and their rank.
    [{'text': 'SaaS Payroll Options', 'relevance': '0.997853'}, {'text': 'Enterprise Organization
    http://bit.ly/1hOTMMV', 'relevance': '0.716868'}, {'text': 'Startups', 'relevance': '0.475031'}]
  """

  params = {"outputMode": "json", "apikey": _alchemy_key, "text": text}
  alchemy_response = requests.get(ALCHEMY_KEYWORD_PROCESS_URL, params=params)
  result = alchemy_response.json()

  try:
    ret_val = result['keywords']
  except:
    ret_val = None

  return ret_val
