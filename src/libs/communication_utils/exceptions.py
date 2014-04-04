class EmailParseError(Exception):
  """Some kind of problem with creating an email."""
  pass

class InvalidOutboundEmailError(Exception):
  """Some kind of problem sending an email. Ex: they're domain is not valid"""
  pass
