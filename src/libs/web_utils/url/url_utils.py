from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from src.libs.text_utils.summarizer import summarizer_utils


def get_unique_urls_from_iterable(websites):
  return list(set(websites))


def summarize_websites_from_iterable(websites):
  cleaned_websites = []
  for url in websites:
    summary = summarize_text_from_url(url, 2)
    cleaned_websites.extend([{'url': url, 'summary': summary}])
  return cleaned_websites


def summarize_text_from_url(url, sentences_count, _language='english', _summarizer_util=summarizer_utils):
  parser = HtmlParser.from_url(url, Tokenizer(_language))
  return _summarizer_util.summarize_text(parser.document, sentences_count, _language)
