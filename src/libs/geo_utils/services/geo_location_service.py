import sys
from pygeocoder import Geocoder
from pygeolib import GeocoderError
from src.libs.geo_utils.complete_address import CompleteAddress
from src.libs.geo_utils.signals import location_geocoded


_geocoder = Geocoder()


def _get_address_component(address_components, component):
  try:
    ret_val = next(x['short_name'] for x in address_components if component in x['types'])
  except StopIteration:
    ret_val = None

  return ret_val


def get_geocoded_address(address_str):
  results = _geocoder.geocode(address_str)

  current_module = sys.modules[__name__]

  location_geocoded.send(current_module)

  address_components = results.data[0]['address_components']

  address1 = _get_address_component(address_components, 'street_number')
  if not address1:
    address1 = _get_address_component(address_components, 'route')

  address2 = _get_address_component(address_components, 'subpremise')

  city = _get_address_component(address_components, 'sublocality')
  if not city:
    city = _get_address_component(address_components, 'locality')

  #manhattan is not legally a city, but google geocoder thinks it is.
  if city and city.lower() == 'manhattan': city = 'New York'

  state = _get_address_component(address_components, 'administrative_area_level_1')
  zip_code = _get_address_component(address_components, 'postal_code')

  return CompleteAddress(results.latitude, results.longitude, address1, address2, city, state,
                         zip_code, results.formatted_address)

def get_country(location):
  try:
    results = _geocoder.geocode(location)
    ret_val = results[0].country
  except GeocoderError:
    ret_val = None

  return ret_val
