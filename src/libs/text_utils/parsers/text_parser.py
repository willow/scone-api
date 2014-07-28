import logging
from bs4 import BeautifulSoup
from src.libs.text_utils.CanonicalNameResult import CanonicalNameResult
from src.libs.text_utils.formatting.text_formatter import only_alpha_numeric
import html.parser

logger = logging.getLogger(__name__)

def get_canonical_name_from_keywords(content, keywords):
  ret_val = []

  content_alnum = only_alpha_numeric(content).lower()
  content_words = [only_alpha_numeric(x) for x in content.lower().split()]

  for k, v in list(keywords.items()):
    if " " in k:
      if only_alpha_numeric(k).lower() in content_alnum:
        ret_val.append(CanonicalNameResult(v, True))
    elif only_alpha_numeric(k).lower() in content_words:
      ret_val.append(CanonicalNameResult(v, True))

  return list(set(ret_val))

def unescape_html(text):
  return html.unescape(text)

def strip_html(text):
  soup = BeautifulSoup(text)
  return soup.get_text()

def strip_html_from_iterable(iterable):
  ret_val = []
  
  for string in iterable:
    ret_val.append(strip_html(string))
    
  return ret_val

def retrieve_urls_from_text(text):
  soup = BeautifulSoup(text)
  links = soup.find_all('a')

  return [link['href'] for link in links]

def format_https_links_to_http(link):
  if link.startswith('https://'):
    import re
    return re.sub(r'https', r'http', link)
  else:
    return link
