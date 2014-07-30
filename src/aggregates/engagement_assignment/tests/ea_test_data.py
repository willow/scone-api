from faker import Factory
import factory
from factory import fuzzy
from src.aggregates.client.enums import ClientTypeChoices
from src.aggregates.client.models import Client
import uuid


faker = Factory.create()

class ClientFactory(factory.DjangoModelFactory):
  class Meta:
    model = Client

  client_uid = factory.fuzzy.FuzzyAttribute(uuid.uuid1)
  client_name = factory.fuzzy.FuzzyAttribute(faker.name)
  client_type = factory.fuzzy.FuzzyChoice(ClientTypeChoices)
  enabled = True

