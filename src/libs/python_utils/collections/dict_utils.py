# http://stackoverflow.com/a/485368/173957
import ast
import textwrap


def invert_dict(dict_to_invert):
  inv_map = {}

  for k, v in dict_to_invert.items():
    inv_map.setdefault(v, []).append(k)

  return inv_map


def get_dict_from_string(string):
  return ast.literal_eval(textwrap.dedent(string))


# http://stackoverflow.com/questions/2390827/how-to-properly-subclass-dict-and-override-get-set
class NoEmptyDict(dict):
  def __init__(self, *args, **kwargs):
    self.update(*args, **kwargs)

  def __setitem__(self, key, val):
    if val is not None:
      dict.__setitem__(self, key, val)

  def update(self, *args, **kwargs):
    for k, v in dict(*args, **kwargs).items():
      self[k] = v
