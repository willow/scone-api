from django.conf import settings

import praw

reddit_client = praw.Reddit(user_agent=settings.REDDIT_USER_AGENT)


def get_reddit_client():
  return reddit_client
