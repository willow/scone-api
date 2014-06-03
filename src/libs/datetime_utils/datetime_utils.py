import datetime
from pytz import UTC


def get_utc_from_timestamp(timestamp):
  return datetime.datetime.fromtimestamp(timestamp, tz=UTC)
