from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.utils import get_stop_words


def summarize_text(text, sentences_count, _language='english'):
  if isinstance(text, str):
    text = PlaintextParser.from_string(text, Tokenizer(_language)).document

  stemmer = Stemmer(_language)

  summarizer = Summarizer(stemmer)
  summarizer.stop_words = get_stop_words(_language)

  ret_val = ""
  for sentence in summarizer(text, sentences_count):
    ret_val += str(sentence) + " "

  return ret_val
