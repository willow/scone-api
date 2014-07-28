from celery import chain
from src.aggregates.profile.services import profile_tasks
from src.aggregates.profile.services.account_search_profile_service import is_valid_profile_for_account_search
from src.apps.engagement_discovery.enums import ProviderEnum
from src.apps.engagement_discovery.providers.twitter.services import twitter_engagement_discovery_tasks
from src.libs.social_utils.providers.linkedin import linkedin_client_service
from src.libs.social_utils.providers.twitter.twitter_client_service import get_twitter_profile_external_id


def populate_prospect_child_profile_from_account_search(prospect, account_search_data):
  profiles = prospect.profiles.all()

  if profiles.count() == 1:
    profile = profiles.get()

    if profile.provider_type == ProviderEnum.linkedin:

      if account_search_data.twitter_url:
        twitter_external_id = get_twitter_profile_external_id(account_search_data.twitter_url)

        chain(
          profile_tasks.save_profile_from_provider_info_task.si(
            prospect.id, twitter_external_id,
            ProviderEnum.twitter
          ),
          twitter_engagement_discovery_tasks.discover_engagement_opportunities_from_user_task.s(
            {'since': 'w'})
        ).delay()

    elif profile.provider_type == ProviderEnum.twitter:
      if account_search_data.linkedin_url:
        linkedin_external_id = linkedin_client_service.get_linkedin_profile_external_id(
          account_search_data.linkedin_url)

        profile_tasks.save_profile_from_provider_info_task.delay(
          prospect.id, linkedin_external_id,
          ProviderEnum.linkedin
        )


def get_valid_profile_for_account_search(prospect):
  return next(p for p in prospect.profiles.all() if is_valid_profile_for_account_search(p))
