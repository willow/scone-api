from src.aggregates.engagement_assignment import constants
from src.aggregates.engagement_assignment.calculation.calculation_data_providers.base_calculation_data_provider import \
  BaseCalculationDataProvider
from src.apps.engagement_discovery.enums import ProviderActionEnum


class RedditCalculationDataProvider(BaseCalculationDataProvider):
  def provide_calculation_data(self, client, engagement_opportunity):
    ret_val = super().provide_calculation_data(client, engagement_opportunity)

    eo_attrs = engagement_opportunity.engagement_opportunity_attrs
    profile_attrs = engagement_opportunity.profile.profile_attrs

    ret_val[constants.NAME] = profile_attrs.get(constants.NAME)
    ret_val[constants.BIO] = profile_attrs.get(constants.BIO)
    ret_val[constants.BIO_TA_TOPIC_SCORE_MULTIPLIER] = 0

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
    ret_val[constants.EO_WEBSITE_TA_TOPIC_SCORE_MULTIPLIER] = 3
    ret_val[constants.PROFILE_WEBSITES] = profile_attrs.get(constants.PROFILE_WEBSITES)
    ret_val[constants.CREATED_DATE] = engagement_opportunity.created_date

    if engagement_opportunity.provider_action_type in (ProviderActionEnum.reddit_link_post,
                                                       ProviderActionEnum.reddit_self_post):

      ret_val[constants.SUBMISSION_OWNER] = True
    else:
      ret_val[constants.SUBMISSION_OWNER] = False

    ret_val[constants.SUBMISSION_OWNER_SCORE_MULTIPLIER] = 3

    ret_val[constants.FOLLOWERS_COUNT] = profile_attrs.get(constants.FOLLOWERS_COUNT)

    return ret_val
