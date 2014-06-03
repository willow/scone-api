from readability.readability import Document
import requests


def get_main_content_from_web_page(url):
  text = requests.get(url).text
  doc = Document(text)
  return doc.summary()
