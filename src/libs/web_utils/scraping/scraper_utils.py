from django.conf import settings
from readability.readability import Document
import requests

from contextlib import closing


def get_main_content_from_web_page(url):
  with closing(requests.get(url, stream=True, timeout=settings.HTTP_TIMEOUT)) as r:
    content_type = r.headers['content-type']
    if not content_type.lower().startswith('text'):
      raise ValueError("Invalid content type: %s" % content_type)

    doc = Document(r.text)

  # noinspection PyUnboundLocalVariable
  # we want to release the connection immediately.
  return doc.summary()
