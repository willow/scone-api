def event_idempotent(func):
  func.is_idempotent = True

  return func
