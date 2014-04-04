import logging
from src.libs.text_utils.CanonicalNameResult import CanonicalNameResult
from src.libs.text_utils.formatting.text_formatter import only_alpha_numeric

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
