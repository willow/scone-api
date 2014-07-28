from bs4 import BeautifulSoup
import contextlib
import re
from src.libs.social_utils.providers.linkedin import linkedin_client_provider
from urllib.request import urlopen


def get_linkedin_profile_external_id(linkedin_url):
  if '/profile/' in linkedin_url:
    raise ValueError('public profile id required')

  elif '/in/' in linkedin_url:
    p = re.compile('(/in/.+)')

  elif '/pub/' in linkedin_url:
    p = re.compile('(/pub/.+)')

  else:
    raise ValueError('invalid url')

  external_id = p.findall(linkedin_url)
  return external_id[0]


def get_linkedin_public_url(external_id):
  member_url = 'http://www.linkedin.com' + str(external_id)
  return member_url


def get_linkedin_profile_data_from_id(external_id, selectors, _linkedin_client_provider=None):
  if not _linkedin_client_provider: _linkedin_client_provider = linkedin_client_provider

  client = _linkedin_client_provider.get_linkedin_client()

  member_url = get_linkedin_public_url(external_id)

  profile_data = client.get_profile(member_url=member_url, selectors=selectors)

  return profile_data


def get_linkedin_company_data_from_id(company_id, selectors, _linkedin_client_provider=None):
  if not _linkedin_client_provider: _linkedin_client_provider = linkedin_client_provider

  client = _linkedin_client_provider.get_linkedin_client()

  company_data = client.get_companies(company_ids=[company_id], selectors=selectors)

  company_data = company_data['values'][0]

  return company_data


# the member_id is not provided via the api, so it must be scraped
# this is the https://www.linkedin.com/profile/view?id=[123234345] <- that id
def get_linkedin_view_id(public_profile_url):
  with contextlib.closing(urlopen(public_profile_url)) as html:
    soup = BeautifulSoup(html)

    raw = str(soup.find('script', text=re.compile('bcookie')))

    p = re.compile("newTrkInfo\s*=\s*'(\d+),")

    ret_val = p.findall(raw)[0]

    return ret_val
