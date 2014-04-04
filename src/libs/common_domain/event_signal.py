from django.dispatch import Signal


class EventSignal(Signal):
  def __init__(self, name, module_name, version, providing_args=None):
    super(EventSignal, self).__init__(providing_args)
    self.name = name
    self.module_name = module_name
    self.version = version
