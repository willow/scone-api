from django.conf import settings

import praw

reddit_client = praw.Reddit(user_agent=settings.REDDIT_USER_AGENT, timeout=settings.HTTP_TIMEOUT,
                            disable_update_check=True)


def get_reddit_client():
  return reddit_client
