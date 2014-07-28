from contextlib import closing
from django.conf import settings
import re
import requests
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from src.libs.text_utils.summarizer import summarizer_utils
import logging

logger = logging.getLogger(__name__)


def get_unique_urls_from_iterable(websites):
  return list(set(websites))


def summarize_websites_from_iterable(websites):
  cleaned_websites = []
  for url in websites:
    try:
      summary = summarize_text_from_url(url, 2)
      cleaned_websites.append({'url': url, 'summary': summary})
    except Exception:
      logger.debug("Error summarizing website", exc_info=True)
      continue
  return cleaned_websites


def summarize_text_from_url(url, sentences_count, _language='english', _summarizer_util=summarizer_utils):
  with closing(requests.get(url, stream=True, timeout=settings.HTTP_TIMEOUT)) as r:

    content_type = r.headers['content-type']

    if not content_type.lower().startswith('text'):
      raise ValueError("Invalid content type: %s" % content_type)

    parser = HtmlParser.from_string(r.text, url, Tokenizer(_language))

    return _summarizer_util.summarize_text(parser.document, sentences_count, _language)


web_scheme_pattern = re.compile(r'http(s?)\://', re.IGNORECASE)


def normalize_url(url):
  if not web_scheme_pattern.match(url):
    url = 'http://' + url

  return url
