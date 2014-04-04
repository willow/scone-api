# -*- coding: utf-8 -*-

import pytest
from src.libs.housing_utils.parsing import home_parser


@pytest.mark.parametrize(("input_values", "expected"), [
  ('studio', 0),
  ('1br', 1),
  ('$5300 / 3br - 1500ft - W-O-N-D-E-R-F-U-L APT____Doorman, Roofdeck/GYM - NO FEE!!! (East Village', 3),
  ('$2750 / 400ft - Bright studio with great closet space and city view (Midtown West)', 0),
  ('Rental Upper West Side 2 rooms studio 1 bath', 0),
  ('Multi-family Upper West Side 580 ft² $52 per ft² 1 bed 1 bath', 1),
])
def test_home_parser_detects_correct_bedroom_count(input_values, expected):
  assert expected == home_parser.get_bedroom_count(input_values)

@pytest.mark.parametrize(("input_values", "expected"), [
  ('1 bath', 1),
  ('$6400 / 4br - 1510ft - MASSIVE TRUE 4BDS/2BATHS~~48 ST~~W.D IN THE UNIT~~1ST AVE~~1500 S (Midtown East)', 2),
  ('Rental Upper West Side 2 rooms studio 1 bath', 1),
])
def test_home_parser_detects_correct_bathroom_count(input_values, expected):
  assert expected == home_parser.get_bathroom_count(input_values)

@pytest.mark.parametrize(("input_values", "expected"), [
  ('$6400 / 4br - 1510ft - MASSIVE TRUE 4BDS/2BATHS~~48 ST~~W.D IN THE UNIT~~1ST AVE~~1500 S (Midtown East)', 1510.0),
  ('Multi-family Upper West Side 580 ft² $52 per ft² 1 bed 1 bath', 580),
])
def test_home_parser_detects_correct_sqfeet(input_values, expected):
  assert expected == home_parser.get_sqfeet(input_values)

@pytest.mark.parametrize(("input_values", "expected"), [
  ('$6400 / 4br - 1510ft - MASSIVE TRUE 4BDS/2BATHS~~48 ST~~W.D IN THE UNIT~~1ST AVE~~1500 S (Midtown East)', 6400.0),
  ('$3,750', 3750.0),
])
def test_home_parser_detects_correct_price(input_values, expected):
  assert expected == home_parser.get_price(input_values)

@pytest.mark.parametrize(("input_values", "expected"), [
  ('http://newyork.craigslist.org/mnh/fee/3995786968.html', True),
  ('http://newyork.craigslist.org/brk/abo/3981928312.html', False),
])
def test_home_parser_detects_correct_broker_fee(input_values, expected):
  assert expected == home_parser.get_broker_fee_from_url(input_values)
