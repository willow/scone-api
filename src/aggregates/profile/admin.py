from celery import chain
import json
from src.aggregates.profile.services import profile_tasks
from django.contrib import admin
from django.http.response import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from src.aggregates.profile import constants
from src.aggregates.profile.forms.add_profile_by_url import AddProfileByUrlForm

from src.aggregates.profile.models import Profile
from src.aggregates.prospect.services import prospect_tasks
from src.aggregates.topic.models import Topic
from src.apps.engagement_discovery.enums import ProviderEnum
from src.libs.social_utils.providers.linkedin import linkedin_client_service


class ProfileAdmin(admin.ModelAdmin):
  actions = None
  readonly_fields = ('profile_uid',)

  def has_delete_permission(self, request, obj=None):
    return False

  def has_add_permission(self, request):
    return False

  # Allow viewing objects but not actually changing them
  # https://gist.github.com/aaugustin/1388243
  def has_change_permission(self, request, obj=None):
    if request.method not in ('GET', 'HEAD'):
      return False
    return super().has_change_permission(request, obj)

  def get_readonly_fields(self, request, obj=None):
    return self.fields or [f.name for f in self.model._meta.fields]


admin.site.register(Profile, ProfileAdmin)


def add_profile_by_url(request, *args, **kwargs):
  template_path = 'add_profile_by_url.html'

  if request.method == 'POST':
    post_data = AddProfileByUrlForm(request.POST)

    if post_data.is_valid():

      topic_types = [int(x) for x in post_data.cleaned_data['topic_types']]

      url_input = post_data.cleaned_data['url']

      def standard_key_names_hook(dct):
        return {k.lower(): v for k, v in dct.items()}

      try:
        urls = json.loads(url_input, object_hook=standard_key_names_hook)
        urls = [v for x in urls for k, v in x.items() if k == "public profile url" and v not in ("null", "")]
      except:
        urls = url_input.splitlines()

      for url in urls:

        provider_type = ProviderEnum.get_from_url(url)

        if provider_type == ProviderEnum.linkedin:
          external_id = linkedin_client_service.get_linkedin_profile_external_id(url)
          get_prospect = prospect_tasks.save_prospect_from_provider_info_task.s(
            external_id,
            provider_type
          )

          save_profile = profile_tasks.save_profile_from_provider_info_task.s(
            external_id, provider_type, {constants.TOPIC_IDS: topic_types}
          )

          chain(
            get_prospect,
            save_profile
          ).delay()
        else:
          return HttpResponseServerError("Only linkedin can be added this way right now")
    else:
      return render(request, template_path, {'form': post_data})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  else:
    form = AddProfileByUrlForm()
    return render(request, template_path, {'form': form})


admin.site.register_view('Add Profile by URL', view=add_profile_by_url)
