from django.conf import settings
from linkedin import linkedin

auth = linkedin.LinkedInDeveloperAuthentication(
  consumer_key=settings.LINKEDIN_API_KEY,
  consumer_secret=settings.LINKEDIN_API_SECRET,
  user_token=settings.LINKEDIN_USER_TOKEN,
  user_secret=settings.LINKEDIN_USER_SECRET,
  redirect_uri=settings.LINKEDIN_REDIRECT_URI
)

linkedin_client = linkedin.LinkedInApplication(auth)

def get_linkedin_client():
  return linkedin_client
