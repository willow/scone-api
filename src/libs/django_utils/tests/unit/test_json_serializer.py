import datetime
import json

from dateutil.tz import tzoffset
from src.libs.django_utils.serialization.flexible_json_serializer import JSONSerializer
from src.libs.django_utils.tests import FakeTestClass


def test_serializer_serializes_dict_with_model():
  serializer = JSONSerializer()
  test_class = FakeTestClass(name='Some Name', id=1, url='http://www.test.com', trusted_geo_data=False)
  dict_data = {'attrs': {'city': 'Brooklyn', 'posted_date': datetime.datetime(2013, 8, 29, 12, 55,
                                                                               tzinfo=tzoffset('EDT', -14400)),
                         'description': 'Beautiful 3 Bedroom 2 Full bath\n\nAmazing Finishes\n\nHuge '
                                        'Backyard\n\n100% no fee By owner\n\nAll Bedrooms can fit King and Queen '
                                        'sized beds\n\nSteps to the G train\n\nLaundry in the Building\n\nClose to '
                                        'All your needs\n\nNo brokers Please\n\nCall or Text Danny @ 646 338 '
                                        '3852\n\n3526+56+5',
                         'title': '$2695 / 3br - 3 Bedroom 2 Full bath + Massive Backyard~Prime Location (bedstuy / '
                                  'clinton hill)',
                         'url': 'http://newyork.craigslist.org/brk/abo/4033538277.html', 'broker_fee': False,
                         'price': 2695.0, 'state': 'NY', 'contact_phone_number': '(646) 338-3852',
                         'address': 'Nostrand Avenue & Vernon Avenue', 'lat': 40.6942608, 'bedroom_count': 3,
                         'lng': -73.9523367,
                         'formatted_address': 'Nostrand Avenue & Vernon Avenue, Brooklyn, NY 11205, USA',
                         'contact_name': 'bedstuy / clinton hill', 'listing_source': test_class, 'zip_code': '11205'}}

  serialized_data = serializer.default(dict_data)
  deserialized_data = json.loads(serialized_data)
  x = deserialized_data

def test_serializer_serializes_model_correctly():
  serializer = JSONSerializer()
  test_class = FakeTestClass(name='Some Name', id=1, url='http://www.test.com', trusted_geo_data=False)
  dict_data = {'test_model': test_class}

  serialized_data = serializer.default(dict_data)
  deserialized_data = json.loads(serialized_data)
  assert deserialized_data["test_model"]["model"] == 'django_utils.faketestclass'
