from datetime import timedelta
import re
from dateutil.parser import parse
from django.utils import timezone
from src.libs.datetime_utils.timezone_abbreviations import time_zone_abbreviations

number_with_keyword_pattern = re.compile(r'(?<!\$)(\d+)\s+(\w+)')


def _parse_with_timezones(datetime_str):
  ret_val = parse(datetime_str, tzinfos=time_zone_abbreviations)
  if not ret_val.tzinfo:
    ret_val = ret_val.replace(tzinfo=timezone.utc)
  return ret_val


def get_datetime(datetime_str, _datetime_service=timezone):
  number_with_keyword_result = number_with_keyword_pattern.search(datetime_str)

  if number_with_keyword_result:
    try:
      timedelta_kwargs = {number_with_keyword_result.groups()[1]: float(number_with_keyword_result.groups()[0])}
      ret_val = _datetime_service.now() - timedelta(**timedelta_kwargs)
    except TypeError:
      ret_val = _parse_with_timezones(datetime_str)
  else:
    ret_val = _parse_with_timezones(datetime_str)

  return ret_val
