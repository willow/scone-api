import pytest
from src.libs.geo_utils.parsing import address_parser


@pytest.mark.parametrize(("input_values", "expected"), [
  ('123 fake st', True),
  ('100 e 55th', True),
  ('5th', False),
  ('5th and 55th', False),
  ('St John''s Place', False),
])
def test_address_parser_detects_correct_street_addresses(input_values, expected):
  assert expected == address_parser.is_street_address(input_values)


@pytest.mark.parametrize(("input_values", "expected"), [
  ('62nd at york', True),
  ('21 and broadway', True),
  ('Macon st at Marcy ave', True),
  ('Macon st & Marcy ave', True),
  ('67 w 58th', False),
  ('250 e66', False),
])
def test_address_parser_detects_correct_cross_street_addresses(input_values, expected):
  assert expected == address_parser.is_cross_street_address(input_values)


@pytest.mark.parametrize(("input_values", "expected"), [
  ('123 fake st #99', '#99'),
  ('123 fake st', None),
  ('Some place ste 67', 'ste 67'),
  ('Some place apt. 55', 'apt. 55'),
])
def test_address_parser_detects_address2(input_values, expected):
  assert expected == address_parser.get_address2(input_values)


def test_address_parser_joins_cross_street():
  assert 'Foo & Bar' == address_parser.join_cross_street(('Foo', 'Bar'))


@pytest.mark.parametrize(("input_values", "expected"), [
  ('1886 Park Avenue in Central Harlem, New York, NY 10035', {
    'address1': '1886 Park Avenue',
    'city': 'New York',
    'state': 'NY',
    'zip_code': '10035',
    'formatted_address': '1886 Park Avenue, New York, NY 10035',
  }),
  ('Bergen Street in Crown Heights, Brooklyn, NY 11238', {
    'address1': 'Bergen Street',
    'city': 'Brooklyn',
    'state': 'NY',
    'zip_code': '11238',
    'formatted_address': 'Bergen Street, Brooklyn, NY 11238',
  }),
  ('East 67th Street, New York, NY 10065', {
    'address1': 'East 67th Street',
    'city': 'New York',
    'state': 'NY',
    'zip_code': '10065',
    'formatted_address': 'East 67th Street, New York, NY 10065'
  }),
])
def test_address_parser_parses_well_formatted_address(input_values, expected):
  complete_address = address_parser.parse_address(input_values)._asdict()
  for k, v in list(expected.items()):
    assert complete_address[k] == v


@pytest.mark.parametrize(("input_values"), [
  '1886 Park Avenue in Central Harlem, New York, NY',
  '1886 Park Avenue in Central Harlem, New York, 10035',
  '1886 Park Avenue in Central Harlem, NY 10035',
  'New York, NY 10035',
])
def test_address_parser_throws_appropriate_error_for_missing_component(input_values):
  with pytest.raises(ValueError):
    address_parser.parse_address(input_values)

