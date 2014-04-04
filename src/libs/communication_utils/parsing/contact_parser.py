import re
import logging
from src.libs.text_utils.formatting.text_formatter import unescape, despacify, decodeJs

specific_phone_number_pattern = re.compile(
  r'(1[\W_]*)?(?P<whole>(?P<area_code>[2-9]\d{2})[\W_]*(?P<exchange>\d{3})[\W_]*(?P<number>\d{4}))'
)
vague_phone_number_pattern = re.compile(
  r'(1[\W_]*)?(?P<proto_phone_number>[2-9][\W_]*(?:\d[\W_]*){8}\d)'
)

logger = logging.getLogger(__name__)


def get_contact_name(contact_name_str):
  ret_val = contact_name_str.strip()
  return ret_val


def get_contact_phone_number(phone_number_str):
  phone_number = None

  # Filter out potentially confounding artifacts in the text, like links.
  filtered_text = re.sub(r'https?://\S*', '--url--', phone_number_str)

  try:
    # Old way of finding phone numbers.
    old_phone_number_components = specific_phone_number_pattern.search(filtered_text)
    if old_phone_number_components:
      phone_number = "({0}) {1}-{2}".format(old_phone_number_components.group('area_code'),
                                             old_phone_number_components.group('exchange'),
                                             old_phone_number_components.group('number'))
    else:
      # New way of finding phone numbers.
      new_phone_number_components = vague_phone_number_pattern.search(filtered_text)
      if new_phone_number_components:
        phone_number = "({0}{1}{2}) {3}{4}{5}-{6}{7}{8}{9}".format(
          *(x for x in new_phone_number_components.group('proto_phone_number') if x.isalnum()))
  except:
    logger.warn("Error parsing phone number: {0}".format(phone_number_str), exc_info=1)

  return phone_number


def get_contact_email_address(contact_email_address_str):
  email_address = None
  # Adapted from http://jasonpriem.org/obfuscation-decoder/.
  # decode html entities
  text = unescape(contact_email_address_str)

  # remove tags
  # This unfortunately removes <a href="mailto:xyz@abc.com">
  text = re.sub(r'<[^>]+>', r'', text)

  # mark all periods as periods, so that they don't look like dots
  text = re.sub(r'\b\.\s', '[PERIOD] ', text)

  # despacify text
  text = despacify(text)

  # find the "dot"
  text = re.sub(r'[^A-Z0-9\-]*\.[^A-Z0-9\-]*|\W+dot\W+|\W+d0t\W+', r'.', text, flags=re.IGNORECASE)
  text = re.sub(r'([a-z0-9])DOT([a-z0-9])', r'\1.\2', text)
  text = re.sub(r'([A-Z0-9])dot([A-Z0-9])', r'\1.\2', text)

  # find the "at"
  text = re.sub(r'\W*@\W*|\W+at\W+', r'@', text, flags=re.IGNORECASE)
  text = re.sub(r'([a-z0-9])AT([a-z0-9])', r'\1@\2', text)
  text = re.sub(r'([A-Z0-9])at([A-Z0-9])', r'\1@\2', text)

  # get rid of obfuscating phrases; if the offending phrase includes the "at" or "dot," we have to put that back
  text = re.sub(r'[_\W]*n[_\W]*(o|0)[_\W]*(s|5)[_\W]*p[_\W]*a[_\W]*m[_\W]*', _deobfuscate_phrase, text,
                flags=re.IGNORECASE)

  # decode simple javascript fromCharCode obfuscations
  text = decodeJs(text)

  # pull out the now-standardized email address and return it
  try:
    email_address = re.compile(
      r'\b[A-Z0-9\._\-]+@[A-Z0-9\.\-]+\.(?:[A-Z]{'
      r'2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)\b',

      flags=re.IGNORECASE).search(text).group(0)
    if 'www.' in email_address:
      # This handles the highly unusual case where the text reads: "Find your next apartment at www.dwellee.com."
      # That would parse to apartment@www.dwellee.com.
      email_address = None
  except:
    logger.warn("Error parsing email: {0}".format(contact_email_address_str), exc_info=1)

  return email_address


def _deobfuscate_phrase(match):
  text = match.group(0)
  if '.' in text: return '.'
  if '@' in text: return '@'
  return ''

