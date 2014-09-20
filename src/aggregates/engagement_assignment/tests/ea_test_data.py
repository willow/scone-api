from django.utils import timezone
from faker import Factory
import factory
from factory import fuzzy
import uuid

from src.aggregates.client.enums import ClientTypeChoices
from src.aggregates.client.models import Client
from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.models import EngagementAssignment
from src.aggregates.engagement_opportunity.models import EngagementOpportunity
from src.aggregates.profile.models import Profile
from src.aggregates.prospect.models import Prospect
from src.apps.engagement_discovery.enums import ProviderChoices, ProviderActionChoices, ProviderEnum


faker = Factory.create()

str_uid = lambda: str(uuid.uuid1())

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


client_1 = ClientFactory.build()
# endregion aggregates

# region score_attrs data

# **Example Format**
# ******************
# {
# 'prospect': {
# 'internal_score_attrs': {},
# 'internal_score': 0,
# 'base_score_attrs': {
# 'new_prospect_score': 1,
# 'relative_dob_score': 1
# },
# 'base_score': 2,
# 'uid': 1
# },
# 'profiles': [{
# 'provider_type': 1,
# 'internal_score': 0,
# 'base_score': 0,
# 'internal_score_attrs': {},
# 'base_score_attrs': {},
# 'uid': 1
# }],
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


class EngagementOpportunityScoreFactory(BaseScoreFactory):
  pass


class ScoreAttrsFactory(factory.Factory):
  class Meta:
    model = dict

  prospect = factory.SubFactory(ProspectScoreFactory)
  profiles = factory.List([factory.SubFactory(ProfileScoreFactory)])
  assigned_entities = factory.List([factory.SubFactory(EngagementOpportunityScoreFactory)])


assignment_1 = ScoreAttrsFactory.build(
  prospect__base_score=2,
  prospect__base_score_attrs={
    constants.RELATIVE_DOB_SCORE: 1,
    constants.LOCATION_SCORE: 1,
  },
  profiles__0=ProfileScoreFactory.build(
    provider_type=ProviderEnum.twitter,
    base_score=5,
    base_score_attrs={
      constants.RECENT_TWEET_TA_TOPIC_KEYWORD_SCORE: 5
    }
  ),
  assigned_entities__0=EngagementOpportunityScoreFactory.build(
    provider_type=ProviderEnum.twitter,
    entity_type=constants.EO,
    base_score=3,
    base_score_attrs={
      constants.TWEET_TEXT_TA_TOPIC_KEYWORD_SCORE: 3
    }
  )
)

assignment_2 = ScoreAttrsFactory.build(
  profiles__0=ProfileScoreFactory.build(
    provider_type=ProviderEnum.reddit,
    base_score=5,
    base_score_attrs={
      constants.RECENT_COMMENT_TA_TOPIC_KEYWORD_SCORE: 5
    }
  ),
  assigned_entities__0=EngagementOpportunityScoreFactory.build(
    provider_type=ProviderEnum.reddit,
    entity_type=constants.EO,
    base_score=5,
    base_score_attrs={
      constants.COMMENT_TEXT_TA_TOPIC_KEYWORD_SCORE: 5
    }
  )
)


# endregion score_attrs data

# region score_data_provider_data
client_1_score_data = {
  constants.PROSPECT_UPPER_BOUND_SCORE: 8,
  ProviderEnum.twitter: {
    constants.PROFILE_UPPER_BOUND_SCORE: 10,
    constants.ENGAGEMENT_OPPORTUNITY_UPPER_BOUND_SCORE: 10,
  },
  ProviderEnum.reddit: {
    constants.PROFILE_UPPER_BOUND_SCORE: 10,
    constants.ENGAGEMENT_OPPORTUNITY_UPPER_BOUND_SCORE: 8,
  }
}
# endregion score_data_provider_data
