import resource


def get_process_memory_usage():
  """
  'Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  """
  return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
