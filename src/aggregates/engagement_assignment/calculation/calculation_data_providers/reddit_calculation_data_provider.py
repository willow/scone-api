from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.calculation_data_providers.base_calculation_data_provider import \
  BaseCalculationDataProvider
from src.aggregates.engagement_opportunity.models import EngagementOpportunity
from src.aggregates.topic.enums import TopicCategoryEnum
from src.aggregates.topic.services import topic_service
from src.apps.engagement_discovery.enums import ProviderActionEnum


class RedditCalculationDataProvider(BaseCalculationDataProvider):

  _known_locations = (
    "nyc",
    "london",
    "orangecounty",
  )
    
  def _provide_internal_calculation_data(self, client, assigned_entity):
    
    if not isinstance(assigned_entity, EngagementOpportunity):
      raise ValueError("This data provider only works with EO's")
    else:
      engagement_opportunity = assigned_entity

    ret_val = {}

    eo_attrs = engagement_opportunity.engagement_opportunity_attrs
    profile_attrs = engagement_opportunity.profile.profile_attrs

    ret_val[constants.NAME] = profile_attrs.get(constants.NAME)
    ret_val[constants.BIO] = profile_attrs.get(constants.BIO)
    ret_val[constants.BIO_TA_TOPIC_SCORE_KEYWORD_MULTIPLIER] = 0

    # this is probably better put in the profile_service, but we're not passing in the eo right now there for reddit
    # presumption is: if they're posting r/london (and we found them in r/london), they're probably from london
    for topic in engagement_opportunity.topics.all():
      topic = topic_service.get_topic(topic.topic_type_id)
      for subtopic in topic.subtopics.all():
        for location in self._known_locations:
          if location in subtopic.subtopic_name:
            ret_val[constants.LOCATION] = location
            break
          else:
            ret_val[constants.LOCATION] = profile_attrs.get(constants.LOCATION)

    # we are combining post, comments, subreddits, etc. here for scoring
    recent_posts = []
    recent_comments = profile_attrs.get(constants.RECENT_COMMENTS)
    for comment in recent_comments:
      recent_posts.append(comment['text'])

    recent_submissions = profile_attrs.get(constants.RECENT_SUBMISSIONS)
    for submission in recent_submissions:
      
      recent_posts.append(submission['text'])

    ret_val[constants.RECENT_POSTS] = recent_posts
    ret_val[constants.RECENT_POST_TA_TOPIC_SCORE_MULTIPLIER] = 2
    ret_val[constants.TEXT] = eo_attrs.get(constants.TEXT)
    ret_val[constants.TEXT_HTML] = eo_attrs.get(constants.TEXT_HTML)
    ret_val[constants.EO_WEBSITES] = eo_attrs.get(constants.WEBSITES)
    ret_val[constants.EO_WEBSITE_TA_TOPIC_KEYWORD_SCORE_MULTIPLIER] = 3
    ret_val[constants.PROFILE_WEBSITES] = profile_attrs.get(constants.PROFILE_WEBSITES)
    ret_val[constants.CREATED_DATE] = engagement_opportunity.created_date

    if engagement_opportunity.provider_action_type in (ProviderActionEnum.reddit_link_post,
                                                       ProviderActionEnum.reddit_self_post):

      ret_val[constants.SUBMISSION_OWNER] = True
    else:
      ret_val[constants.SUBMISSION_OWNER] = False

    ret_val[constants.SUBMISSION_OWNER_SCORE_MULTIPLIER] = 3

    ret_val[constants.FOLLOWERS_COUNT] = profile_attrs.get(constants.FOLLOWERS_COUNT)
    ret_val[constants.COMPANY] = profile_attrs.get(constants.COMPANY)
    ret_val[constants.COMPANY_UNIVERSAL_NAME] = profile_attrs.get(constants.COMPANY_UNIVERSAL_NAME)
    ret_val[constants.COMPANY_INDUSTRIES] = profile_attrs.get(constants.COMPANY_INDUSTRIES)
    ret_val[constants.COMPANY_EMPLOYEE_COUNT] = profile_attrs.get(constants.COMPANY_EMPLOYEE_COUNT)
    ret_val[constants.COMPANY_INDUSTRY_SCORE] = profile_attrs.get(constants.COMPANY_INDUSTRY_SCORE)
    ret_val[constants.COMPANY_EMPLOYEE_COUNT_SCORE] = profile_attrs.get(constants.COMPANY_EMPLOYEE_COUNT_SCORE)

    return ret_val
