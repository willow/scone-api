import os
import sys
from django.utils import encoding


def re_throw_ex(ex_type, message, inner_ex):
  return (
    ex_type,
    log_ex_with_message(message, inner_ex),
    sys.exc_info()[2] #this is the traceback
  )


def log_ex_with_message(message, inner_ex):
  return "{0}{sep}Inner Exception: {1}{sep}\t{2}".format(
    message, type(inner_ex), encoding.smart_unicode(inner_ex, errors='ignore'), sep=os.linesep
  )
