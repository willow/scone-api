from django.utils import timezone
from faker import Factory
import factory
from factory import fuzzy
from functools import partial
import uuid

from src.aggregates.client.enums import ClientTypeChoices
from src.aggregates.client.models import Client
from src.aggregates.engagement_assignment.models import EngagementAssignment
from src.aggregates.engagement_opportunity.models import EngagementOpportunity
from src.aggregates.profile.models import Profile
from src.aggregates.prospect.models import Prospect
from src.apps.engagement_discovery.enums import ProviderChoices, ProviderActionChoices


faker = Factory.create()

str_uid = partial(str, uuid.uuid1)

# region aggregates
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

# endregion aggregates

# region score_attrs data

  # **Example Format**
  # ******************
  #   {
  #       'prospect': {
  #           'internal_score_attrs': {},
  #           'internal_score': 0,
  #           'base_score_attrs': {
  #               'new_prospect_score': 1,
  #               'relative_dob_score': 1
  #           },
  #           'base_score': 2,
  #           'uid': 1
  #       },
  #       'profiles': [{
  #           'provider_type': 1,
  #           'internal_score': 0,
  #           'base_score': 0,
  #           'internal_score_attrs': {},
  #           'base_score_attrs': {},
  #           'uid': 1
  #       }],
  #       'assigned_entities': [{
  #           'provider_type': 1,
  #           'internal_score': 0,
  #           'base_score': 0,
  #           'internal_score_attrs': {},
  #           'entity_type': 'engagement_opportunity',
  #           'base_score_attrs': {},
  #           'uid': 1
  #       }]
  #   }

class BaseScoreFactory(factory.Factory):
  class Meta:
    model = dict

  internal_score = 0
  internal_score_attrs = {}
  base_score = 0
  base_score_attrs = {}
  uid = factory.fuzzy.FuzzyAttribute(str_uid)

class ProspectScoreFactory(BaseScoreFactory):
  pass

class ProfileScoreFactory(BaseScoreFactory):
  pass

class ScoreAttrsFactory(factory.Factory):
  class Meta:
    model = dict

  prospect = factory.SubFactory(ProspectScoreFactory)
  profiles = factory.List([factory.SubFactory(ProfileScoreFactory)])
  assigned_entities = factory.List([factory.SubFactory(ProfileScoreFactory)])



prospect_1 = ScoreAttrsFactory.build(
    prospect__base_score_attrs={
      'relative_dob_score': 1,
      'new_prospect_score': 1
    }
  )


# endregion score_attrs data
