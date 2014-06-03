from django.contrib import admin

from src.aggregates.client.models import Client, TATopic
from src.aggregates.client.services import client_service


class TopicInline(admin.TabularInline):
  model = TATopic
  readonly_fields = ('ta_topic_uid',)
  can_delete = False


class ClientAdmin(admin.ModelAdmin):
  actions = None
  readonly_fields = ('client_uid',)
  inlines = [
    TopicInline,
  ]

  def save_model(self, request, obj, form, change):
    if change:
      super().save_model(request, obj, form, change)
    else:
      form.instance = client_service.create_client(obj.client_name, obj.client_type)

  def save_related(self, request, form, formsets, change):
    client = form.instance
    ta_topics_formset = formsets[0]

    save_required = False

    for ta_topic in ta_topics_formset.save(commit=False):
      save_required = True
      client.add_ta_topic(ta_topic.topic_type_id)

    if save_required:
      client_service.save_or_update(client)

  def has_delete_permission(self, request, obj=None):
    return False


admin.site.register(Client, ClientAdmin)
