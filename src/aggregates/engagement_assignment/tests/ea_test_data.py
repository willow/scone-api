import factory
from src.aggregates.client.models import Client
import uuid


class ClientFactory(factory.DjangoModelFactory):
  class Meta:
    model = Client

  client_uid = factory.fuzzy.FuzzyAttribute(uuid.uuid1)



client_1 = ClientFactory.build(

)
