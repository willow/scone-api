import re
from src.libs.geo_utils.complete_address import CompleteAddress

address2_pattern = re.compile(r"((\#|apt|suite|ste)\.?\s?\d+)", re.IGNORECASE)
zip_code_pattern = re.compile(r'^\d{5}(?:-\d{4})?$')
well_formatted_pattern = re.compile(
  r'(?:(?P<building_name>[\w\s\-]+)\s+at\s+)?'
  r'((?P<address_number>[\d\-]+)\s+)?'
  r'(?P<street>([\w\s\-]+(?=\sin))|([\w\s\-]+(?=,)))'
  r'(?: in (?P<neighborhood>[\w\s\-]+))?,\s*'
  r'(?P<city>[\w\s\-\.]+),\s*'
  r'(?P<state>\w{2})\s+'
  r'(?P<zip_code>\d{5})'
)

def is_street_address(address):
  address_split = [address_part for address_part in address.split() if address_part not in ("and", "at")]
  return len(address_split) >= 3 and address_split[0].isdigit()


def is_cross_street_address(address):
  return " and " in address or " at " in address or " & " in address


def join_cross_street(address):
  return ' & '.join(address)

from django.core.mail import send_mail
def is_valid_zip_code(zip_code):
  return bool(zip_code_pattern.search(zip_code))


def get_address2(address):
  ret_val = None

  match = address2_pattern.search(address)

  if match:
    ret_val = match.group()

  return ret_val


def parse_address(address_str):
  r = well_formatted_pattern.search(address_str)

  if not r: raise ValueError('invalid address pattern')

  address_dict = r.groupdict()

  address_number = address_dict['address_number']
  street = address_dict['street']
  address1 = address_number + ' ' + street if address_number else street

  city = address_dict['city']
  state = address_dict['state']
  zip_code = address_dict['zip_code']

  if not address1: raise ValueError('address1 missing')
  if not city: raise ValueError('city missing')
  if not state: raise ValueError('state missing')
  if not zip_code: raise ValueError('zip_code missing')

  formatted_address = '{0}, {1}, {2} {3}'.format(address1, city, state, zip_code)

  complete_address = CompleteAddress(
    lat=None, lng=None, address1=address1, address2=None, city=city, state=state,
    zip_code=zip_code, formatted_address=formatted_address
  )
  return complete_address
