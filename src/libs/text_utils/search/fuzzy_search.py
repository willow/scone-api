from difflib import SequenceMatcher
import operator


def get_closest_word(target, sources):
  matcher = SequenceMatcher(a=target)

  seqs = {}

  for s in sources:
    matcher.set_seq2(s)
    seqs[s] = matcher.real_quick_ratio()

  # http://stackoverflow.com/a/613218/173957
  sorted_seqs = sorted(iter(seqs.items()), key=operator.itemgetter(1), reverse=True)
  return sorted_seqs[0][0]
