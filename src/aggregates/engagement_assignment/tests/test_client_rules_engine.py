from src.aggregates.engagement_assignment.calculation.rules_engine.base_engagement_opportunity_rules_engine import \
  BaseTwitterEngagementOpportunityRulesEngine, BaseRedditEngagementOpportunityRulesEngine, \
  BaseLinkedInEngagementOpportunityRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.base_profile_rules_engine import \
  BaseTwitterProfileRulesEngine, BaseLinkedInProfileRulesEngine, BaseRedditProfileRulesEngine
from src.aggregates.engagement_assignment.calculation.rules_engine.base_prospect_rules_engine import \
  BaseProspectRulesEngine
from src.libs.nlp_utils.services.enums import GenderEnum


class ProspectRulesEngine(BaseProspectRulesEngine):
  @property
  def _important_locations(self):
    return (
      "sf",
      "san fran",
      "nyc",
      "new york",
      "atlanta",
      "seattle",
      "philadelphia",
      "chicago",
      "los angeles",
      "dallas",
      "ft worth",
      "boston",
      "boulder",
      "bend",
    )


  @property
  def _important_home_countries(self):
    return (
      "united states",
    )

  @property
  def _age_range(self):
    return 20, 40

  @property
  def _preferred_gender(self):
    return GenderEnum.male

  @property
  def _important_bio_keywords(self):
    return (
      "ceo",
      "cto",
      "software",
      "developer",
      "engineer",
      "programmer",
      "writer",
      "founder",
      "startup",
    )

  @property
  def _important_websites(self):
    return (
      "linkedin",
      "wordpress",
      "blogspot",
      "about.me",
      "ycombinator",
      "stackoverflow",
      ".io",
    )

  def _get_internal_score(self):
    return 0, {}


class TwitterProfileRulesEngine(BaseTwitterProfileRulesEngine):
  def _get_internal_score(self):
    return 0, {}


class RedditProfileRulesEngine(BaseRedditProfileRulesEngine):
  def _get_internal_score(self):
    return 0, {}


class LinkedInProfileRulesEngine(BaseLinkedInProfileRulesEngine):
  def _get_internal_score(self):
    return 0, {}


class TwitterEngagementOpportunityRulesEngine(BaseTwitterEngagementOpportunityRulesEngine):
  def _get_internal_score(self):
    return 0, {}


class RedditEngagementOpportunityRulesEngine(BaseRedditEngagementOpportunityRulesEngine):
  def _get_internal_score(self):
    return 0, {}


class LinkedInEngagementOpportunityRulesEngine(BaseLinkedInEngagementOpportunityRulesEngine):
  def _get_internal_score(self):
    return 0, {}
