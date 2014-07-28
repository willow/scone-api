from django.contrib import admin

from src.aggregates.client.models import Client, TATopic
from src.aggregates.client.services import client_service


class TopicInline(admin.TabularInline):
  model = TATopic
  readonly_fields = ('ta_topic_uid',)


class ClientAdmin(admin.ModelAdmin):
  readonly_fields = ('client_uid',)
  inlines = [
    TopicInline,
  ]

  def save_model(self, request, obj, form, change):
    if change:
      orig = client_service.get_client_from_id(obj.id)

      if obj.enabled != orig.enabled:
        if obj.enabled:
          obj.enable()
        else:
          obj.disable()
        client_service.save_or_update(obj)

    else:
      form.instance = client_service.create_client(obj.client_name, obj.client_type)

  def save_related(self, request, form, formsets, change):
    client = form.instance
    ta_topics_formset = formsets[0]

    save_required = False

    for ta_topic in ta_topics_formset.save(commit=False):
      save_required = True
      client.add_ta_topic(ta_topic.topic_type_id)

    for ta_topic in ta_topics_formset.deleted_objects:
      save_required = True
      client.remove_ta_topic(ta_topic)

    if save_required:
      client_service.save_or_update(client)

  def delete_model(self, request, obj):
    client_service.delete_client(obj)

  def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)

    form.base_fields['enabled'].initial = True

    return form


admin.site.register(Client, ClientAdmin)
