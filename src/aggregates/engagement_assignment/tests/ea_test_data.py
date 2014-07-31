from django.utils import timezone
from faker import Factory
import factory
from factory import fuzzy
from functools import partial
from src.aggregates.client.enums import ClientTypeChoices
from src.aggregates.client.models import Client
from src.aggregates.engagement_assignment.models import EngagementAssignment
from src.aggregates.engagement_opportunity.models import EngagementOpportunity
from src.aggregates.profile.models import Profile
from src.aggregates.prospect.models import Prospect
from src.apps.engagement_discovery.enums import ProviderChoices, ProviderActionChoices
import uuid


faker = Factory.create()

str_uid = partial(str, uuid.uuid1)


class ClientFactory(factory.DjangoModelFactory):
  class Meta:
    model = Client

  client_uid = factory.fuzzy.FuzzyAttribute(str_uid)
  client_name = factory.fuzzy.FuzzyAttribute(faker.name)
  client_type = factory.fuzzy.FuzzyChoice(ClientTypeChoices)
  enabled = True


class ProspectFactory(factory.DjangoModelFactory):
  class Meta:
    model = Prospect

  prospect_uid = factory.fuzzy.FuzzyAttribute(str_uid)
  prospect_attrs = {}


class ProfileFactory(factory.DjangoModelFactory):
  class Meta:
    model = Profile

  profile_uid = factory.fuzzy.FuzzyAttribute(str_uid)
  profile_external_id = factory.fuzzy.FuzzyAttribute(str_uid)
  provider_type = factory.fuzzy.FuzzyChoice(ProviderChoices)
  profile_attrs = {}
  prospect = factory.SubFactory(ProspectFactory)
  system_created_date = factory.fuzzy.FuzzyAttribute(timezone.now)


class EngagementOpportunityFactory(factory.DjangoModelFactory):
  class Meta:
    model = EngagementOpportunity

  engagement_opportunity_uid = factory.fuzzy.FuzzyAttribute(str_uid)
  engagement_opportunity_external_id = factory.fuzzy.FuzzyAttribute(str_uid)
  engagement_opportunity_attrs = {}
  profile = factory.SubFactory(ProfileFactory, provider_type=factory.SelfAttribute('..provider_type'))
  provider_type = factory.fuzzy.FuzzyChoice(ProviderChoices)
  provider_action_type = factory.fuzzy.FuzzyChoice(ProviderActionChoices)
  created_date = factory.fuzzy.FuzzyAttribute(timezone.now)
  system_created_date = factory.fuzzy.FuzzyAttribute(timezone.now)


class EngagementAssignmentFactory(factory.DjangoModelFactory):
  class Meta:
    model = EngagementAssignment

  engagement_assignment_uid = factory.fuzzy.FuzzyAttribute(str_uid)
  assignment_attrs = {}
  system_created_date = factory.fuzzy.FuzzyAttribute(timezone.now)
  client = factory.SubFactory(ClientFactory)
