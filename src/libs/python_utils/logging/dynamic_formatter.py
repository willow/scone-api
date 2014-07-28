class DynamicFormatter:
  # http://stackoverflow.com/questions/1741972/how-to-use-different-formatters-with-the-same-logging-handler-in-python
  def __init__(self, formatters, default_formatter):
    self._formatters = formatters
    self._default_formatter = default_formatter

  def format(self, record):
    formatter = self._formatters.get(record.name, self._default_formatter)
    return formatter.format(record)
