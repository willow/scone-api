from django.contrib import admin

from src.aggregates.topic.models import Topic, Subtopic
from src.aggregates.topic.services import topic_service


class SubtopicsInline(admin.TabularInline):
  model = Subtopic
  readonly_fields = ('subtopic_uid',)
  can_delete = False


class TopicAdmin(admin.ModelAdmin):
  actions = None
  inlines = [
    SubtopicsInline,
  ]

  def save_model(self, request, obj, form, change):
    if change:
      super().save_model(request, obj, form, change)
    else:
      form.instance = topic_service.create_topic(obj.topic_name)

  def save_related(self, request, form, formsets, change):
    topic = form.instance
    subtopics_formset = formsets[0]

    save_required = False

    for subtopic in subtopics_formset.save(commit=False):
      save_required = True
      topic.associate_subtopic_with_topic(subtopic.subtopic_name, subtopic.category_type)

    if save_required:
      topic_service.save_or_update(topic)

  def has_delete_permission(self, request, obj=None):
    return False

  def get_readonly_fields(self, request, obj=None):
    return list(filter(lambda n: n != "topic_name", self.fields or [f.name for f in self.model._meta.fields]))


admin.site.register(Topic, TopicAdmin)
