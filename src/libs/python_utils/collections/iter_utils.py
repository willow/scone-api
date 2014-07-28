# http://stackoverflow.com/a/312464/173957
from src.libs.text_utils.formatting import text_formatter
from src.libs.text_utils.stemming import stemming_utils


def chunks(l, n):
  """ Yield successive n-sized chunks from l.
  """
  for i in range(0, len(l), n):
    yield l[i:i + n]

class Incrementer():
  def __init__(self):
    self.i = -1

  def increment(self):
    self.i += 1
    return self.i

def stemmify_iterable(iterable, _stemming_util = stemming_utils, _text_formatter = text_formatter):
  ret_val = []
  for keyword in iterable:
    tokens = _text_formatter.tokenize_words(keyword)
    keywords = ''
    for token in tokens:
      keywords += _stemming_util.find_stem(token) + " "
    ret_val.append(keywords.strip())
  return ret_val

# todo: put this in text utils -> stemmify_iterable should call this
def stemmify_string(string, _stemming_util = stemming_utils, _text_formatter = text_formatter):
  tokens = _text_formatter.tokenize_words(string)
  return " ".join([_stemming_util.find_stem(token) for token in tokens])
