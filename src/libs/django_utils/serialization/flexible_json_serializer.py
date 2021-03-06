# http://web.archive.org/web/20120414135953/http://www.traddicts
# .org/webdevelopment/flexible-and-simple-json-serialization-for-django
# http://stackoverflow.com/questions/2249792/json-serializing-django-models-with-simplejson
from datetime import datetime
from io import StringIO
from django.core import serializers
from django.db.models import Model
from django.db.models.query import QuerySet
import collections
from json import dumps
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder


class UnableToSerializeError(Exception):
  """ Error for not implemented classes """

  def __init__(self, value):
    self.value = value
    super().__init__(self)

  def __str__(self):
    return repr(self.value)


class JSONSerializer(JSONEncoder):
  boolean_fields = ['BooleanField', 'NullBooleanField']
  datetime_fields = ['DatetimeField', 'DateField', 'TimeField']
  number_fields = ['IntegerField', 'AutoField', 'DecimalField', 'FloatField', 'PositiveSmallIntegerField']

  def default(self, obj, **options):
    self.options = options

    self.stream = options.pop("stream", StringIO())
    self.selectedFields = options.pop("fields", None)
    self.ignoredFields = options.pop("ignored", None)
    self.use_natural_keys = options.pop("use_natural_keys", False)
    self.currentLoc = ''

    self.django_json_serializer = serializers.get_serializer("json")()

    self.level = 0

    self.start_serialization()

    self.handle_object(obj)

    self.end_serialization()
    return self.getvalue()

  def get_string_value(self, obj, field):
    """Convert a field's value to a string."""
    return field.value_to_string(obj)

  def start_serialization(self):
    """Called when serializing of the queryset starts."""
    pass

  def end_serialization(self):
    """Called when serializing of the queryset ends."""
    pass

  def start_array(self):
    """Called when serializing of an array starts."""
    self.stream.write('[')

  def end_array(self):
    """Called when serializing of an array ends."""
    self.stream.write(']')

  def start_object(self):
    """Called when serializing of an object starts."""
    self.stream.write('{')

  def end_object(self):
    """Called when serializing of an object ends."""
    self.stream.write('}')

  def handle_object(self, object):
    """ Called to handle everything, looks for the correct handling """
    if isinstance(object, dict):
      self.handle_dictionary(object)
    elif isinstance(object, list):
      self.handle_list(object)
    elif isinstance(object, Model):
      self.handle_model(object)
    elif isinstance(object, QuerySet):
      self.handle_queryset(object)
    elif isinstance(object, bool):
      self.handle_simple(object)
    elif isinstance(object, (int, float)):
      self.handle_simple(object)
    elif isinstance(object, str):
      self.handle_simple(object)
    elif object is None:
      self.handle_simple(object)
    elif isinstance(object, datetime):
      self.handle_date(object)
    elif hasattr(object, '_asdict'):
      self.handle_dictionary(object._asdict())
    elif isinstance(object, tuple):
      self.handle_list(object)
    else:
      raise UnableToSerializeError(type(object))

  def handle_dictionary(self, d):
    """Called to handle a Dictionary"""
    i = 0
    self.start_object()
    for key, value in d.items():
      self.currentLoc += key + '.'
      # self.stream.write(unicode(self.currentLoc))
      i += 1
      self.handle_simple(key)
      self.stream.write(': ')
      self.handle_object(value)
      if i != len(d):
        self.stream.write(', ')
      self.currentLoc = self.currentLoc[0:(len(self.currentLoc) - len(key) - 1)]
    self.end_object()

  def handle_list(self, l):
    """Called to handle a list"""
    self.start_array()

    for index, value in enumerate(l):
      self.handle_object(value)
      if index != len(l) - 1:
        self.stream.write(', ')

    self.end_array()

  def handle_model(self, mod):
    """Called to handle a django Model"""
    data = str(self.django_json_serializer.serialize([mod]))
    data = data.lstrip('[').rstrip(']')

    self.stream.write(data)

  def handle_queryset(self, queryset):
    """Called to handle a django queryset"""

    data = str(self.django_json_serializer.serialize(queryset))

    self.stream.write(data)

  def handle_field(self, mod, field):
    """Called to handle each individual (non-relational) field on an object."""
    self.handle_simple(field.name)
    if field.get_internal_type() in self.boolean_fields:
      if field.value_to_string(mod) == 'True':
        self.stream.write(': true')
      elif field.value_to_string(mod) == 'False':
        self.stream.write(': false')
      else:
        self.stream.write(': undefined')
    else:
      self.stream.write(': ')
      self.handle_simple(field.value_to_string(mod))
    self.stream.write(', ')

  def handle_fk_field(self, mod, field):
    """Called to handle a ForeignKey field."""
    related = getattr(mod, field.name)
    if related is not None:
      if field.rel.field_name == related._meta.pk.name:
        # Related to remote object via primary key
        pk = related._get_pk_val()
      else:
        # Related to remote object via other field
        pk = getattr(related, field.rel.field_name)
      d = {
        'pk': pk,
      }
      if self.use_natural_keys and hasattr(related, 'natural_key'):
        d.update({'natural_key': related.natural_key()})
      if isinstance(d['pk'], str) and d['pk'].isdigit():
        d.update({'pk': int(d['pk'])})

      self.handle_simple(field.name)
      self.stream.write(': ')
      self.handle_object(d)
      self.stream.write(', ')

  def handle_m2m_field(self, mod, field):
    """Called to handle a ManyToManyField."""
    if field.rel.through._meta.auto_created:
      self.handle_simple(field.name)
      self.stream.write(': ')
      self.start_array()
      hasRelationships = False
      for relobj in getattr(mod, field.name).iterator():
        hasRelationships = True
        pk = relobj._get_pk_val()
        d = {
          'pk': pk,
        }
        if self.use_natural_keys and hasattr(relobj, 'natural_key'):
          d.update({'natural_key': relobj.natural_key()})
        if isinstance(d['pk'], str) and d['pk'].isdigit():
          d.update({'pk': int(d['pk'])})

        self.handle_simple(d)
        self.stream.write(', ')
      if hasRelationships:
        self.stream.seek(self.stream.tell() - 2)
      self.end_array()
      self.stream.write(', ')

  def handle_simple(self, simple):
    """ Called to handle values that can be handled via simplejson """
    self.stream.write(str(dumps(simple)))

  def handle_date(self, date):
    """ Called to handle values that can be handled via date ISO """
    self.handle_simple(date.isoformat())

  def getvalue(self):
    """Return the fully serialized object (or None if the output stream is  not seekable).sss """
    if isinstance(getattr(self.stream, 'getvalue', None), collections.Callable):
      return self.stream.getvalue()

  def decode(self, s, **kwargs):
    return JSONDecoder().decode(s, **kwargs)
