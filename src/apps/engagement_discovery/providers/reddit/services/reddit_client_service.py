from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone
import praw
from praw.objects import Comment
from src.apps.engagement_discovery import constants
from src.apps.engagement_discovery.enums import ProviderActionEnum, ProviderEnum
from src.apps.engagement_discovery.providers.reddit.reddit_engagement_discovery_objects import \
  RedditEngagementOpportunityDiscoveryObject
from src.libs.datetime_utils.datetime_utils import get_utc_from_timestamp
from src.libs.social_utils.providers.reddit import reddit_client_provider
from src.libs.text_utils.parsers import text_parser
from src.libs.text_utils.parsers.text_parser import strip_html
from src.libs.web_utils.scraping import scraper_utils

import logging

logger = logging.getLogger(__name__)


def _is_valid_redditor(author):
  ret_val = True

  if ret_val:
    recent_comments = author.get_comments(time='month')
    #@todo: this must be removed within the next several days as hpoefully reddit will be fixed
    passing_score = 15
    try:
      author_comments_karma = sum(rc.score for rc in recent_comments)
    except:
      author_comments_karma = passing_score
    if author_comments_karma < 15:
      ret_val = False

  return ret_val


def _is_valid_submission(submission):
  ret_val = True

  if ret_val:
    if submission.score < 1:
      ret_val = False

  if ret_val:
    created = get_utc_from_timestamp(submission.created)
    delta = relativedelta(timezone.now(), created)

    if delta.days > 7:
      ret_val = False

  return ret_val


def _is_redditor_valid_distinct_wrapper(redditor, distinct_redditor_dict):
  redditor_valid = distinct_redditor_dict.get(redditor.name)
  if redditor_valid == None:
    # this is the first time seeing this redditor
    distinct_redditor_dict[redditor.name] = redditor_valid = _is_valid_redditor(redditor)
  return redditor_valid


def _is_valid_comment(comment, _text_parser=None):
  if not _text_parser: _text_parser = text_parser

  ret_val = True

  if ret_val:
    text = comment.body_html
    text = _text_parser.unescape_html(text)

    if len(text) < 150:
      ret_val = False

  return ret_val


def _get_eos_from_submissions(submissions, _text_parser=None, _scraper_utils=None):
  if not _text_parser: _text_parser = text_parser
  if not _scraper_utils: _scraper_utils = scraper_utils

  ret_val = []
  # We can't use set() here because a redditor class doesn't implement __hash__
  # So we have to setup this hack to get unique instances
  distinct_redditor_dict = {}

  for submission in submissions:
    # region return author of submission as eo
    author = submission.author
    redditor_valid = _is_redditor_valid_distinct_wrapper(author, distinct_redditor_dict)

    if redditor_valid:
      # use the selftext_html attr because `selftext` uses markdown and not just plain o'l text.
      text = submission.selftext_html

      # get main content of webpage if not a self post
      if text:
        text = _text_parser.unescape_html(text)
        provider_action = ProviderActionEnum.reddit_self_post
      else:
        try:
          text = _scraper_utils.get_main_content_from_web_page(submission.url)
        except:
          logger.info("Error getting text from reddit link submission", exc_info=True)
          # Don't store this submission.
          continue

        provider_action = ProviderActionEnum.reddit_link_post

      created_at = get_utc_from_timestamp(submission.created_utc)

      # use the body_html attr because `body` uses markdown and not just plain o'l text.
      reddit_obj_attrs = {
        constants.URL: submission.permalink,
        constants.TEXT: strip_html(text),
        constants.TEXT_HTML: text,
      }

      if provider_action == ProviderActionEnum.reddit_link_post:
        reddit_obj_attrs['submission_link'] = submission.url

      ret_val.append(
        RedditEngagementOpportunityDiscoveryObject(
          author.name, submission.id, ProviderEnum.reddit, provider_action, submission, reddit_obj_attrs,
          created_at
        )
      )
    # endregion

    # region return user of comment as eo
    comments = praw.helpers.flatten_tree(submission.comments)

    for comment in comments:
      # comments can be individual comments or type of MoreComments class
      # some comments don't have an author (deleted).
      if isinstance(comment, Comment) and comment.author:

        comment_valid = _is_valid_comment(comment)
        if comment_valid:

          redditor_valid = _is_redditor_valid_distinct_wrapper(comment.author, distinct_redditor_dict)
          author = comment.author

          if redditor_valid:
            # use the body_html attr because `body` uses markdown and not just plain o'l text.
            text = comment.body_html
            text = _text_parser.unescape_html(text)
            created_at = get_utc_from_timestamp(comment.created_utc)
            reddit_obj_attrs = {
              constants.URL: comment.permalink,
              constants.TEXT: strip_html(text),
              constants.TEXT_HTML: text,
            }

            ret_val.append(
              RedditEngagementOpportunityDiscoveryObject(
                author.name, comment.id, ProviderEnum.reddit, ProviderActionEnum.reddit_comment, comment,
                reddit_obj_attrs,
                created_at
              )
            )

    "string here because pycharm won't recognize region otherwise"
    # endregion

  return ret_val


def search_by_subreddit(subreddit_name, _reddit_client_provider=None):
  if not _reddit_client_provider: _reddit_client_provider = reddit_client_provider
  reddit_client = _reddit_client_provider.get_reddit_client()

  # todo find a way to make each post it's own celery request? or, catch timeouts and retry.

  submissions = reddit_client.get_subreddit(subreddit_name).get_hot(limit=settings.REDDIT_SUBREDDIT_QUERY_LIMIT)
  submissions = [submission for submission in submissions if _is_valid_submission(submission)]

  eos_from_submissions = _get_eos_from_submissions(submissions)
  return eos_from_submissions

def _get_reddit_post_websites(reddit_eo, _text_parser=None):
  if not _text_parser: _text_parser = text_parser
  return _text_parser.retrieve_urls_from_text(reddit_eo)
