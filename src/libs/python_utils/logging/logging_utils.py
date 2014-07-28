from contextlib import contextmanager


@contextmanager
def log_wrapper(log_method, msg, *args, **kwargs):
  log_method("Beginning: " + msg, *args, **kwargs)
  yield
  log_method("Completed: " + msg, *args, **kwargs)
