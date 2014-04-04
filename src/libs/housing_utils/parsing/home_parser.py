import re
import logging

bedroom_pattern = re.compile(r"(\d+)\s*(?:br|bed)", re.IGNORECASE)
bathroom_pattern = re.compile(r"([\d\.]+)(.)?bath(.)*", re.IGNORECASE)
sqfeet_pattern = re.compile(r"(\d+)\s*ft", re.IGNORECASE)
price_pattern = re.compile(r"\$(\S+)", re.IGNORECASE)

logger = logging.getLogger(__name__)


def get_bedroom_count(bedroom_str):
  ret_val = None
  if 'studio' in bedroom_str.lower():
    ret_val = 0
  else:
    match = bedroom_pattern.search(bedroom_str)
    if match:
      try:
        ret_val = int(match.groups()[0])
      except:
        logger.warn("Error casting bedroom count: {0}".format(bedroom_str), exc_info=1)
  return ret_val


def get_bathroom_count(bathroom_str):
  ret_val = None
  match = bathroom_pattern.search(bathroom_str)
  if match:
    try:
      ret_val = float(match.groups()[0])
    except:
      logger.warn("Error casting bathroom count: {0}".format(bathroom_str), exc_info=1)

  return ret_val


def get_sqfeet(sqfeet_str):
  ret_val = None
  match = sqfeet_pattern.search(sqfeet_str)
  if match:
    try:
      ret_val = float(match.groups()[0])
    except:
      logger.warn("Error casting sqfeet count: {0}".format(sqfeet_str), exc_info=1)

  return ret_val


def get_price(price_str):
  price_str = price_str.replace(',', '')
  ret_val = None
  match = price_pattern.search(price_str)
  if match:
    try:
      ret_val = float(match.groups()[0])
    except:
      logger.warn("Error casting price count: {0}".format(price_str), exc_info=1)

  return ret_val


def get_broker_fee_from_url(url):
  ret_val = 'fee' in url.split('/')

  return ret_val
