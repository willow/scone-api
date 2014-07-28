from django.contrib import admin

from src.aggregates.topic.models import Topic, Subtopic
from src.aggregates.topic.services import topic_service


class SubtopicsInline(admin.TabularInline):
  model = Subtopic
  # note, subtopic_attrs needs to be read-only because I was getting django errors. The 2nd and 3rd rows in the admin
  # were required to be filled in even tho i just wanted to leave them blank.
  readonly_fields = ('subtopic_uid', )

  def get_formset(self, request, obj=None, **kwargs):
    formset = super().get_formset(request, obj, **kwargs)

    # hack because jsonfield doesn't work with default={} and django 1.7 migrations
    formset.form.base_fields['subtopic_attrs'].initial = {}

    return formset


class TopicAdmin(admin.ModelAdmin):
  inlines = [
    SubtopicsInline,
  ]

  def save_model(self, request, obj, form, change):
    if change:
      if form.has_changed():
        changed_data = {k: form.cleaned_data[k] for k in form.changed_data}
        topic_service.update_attrs(obj, changed_data)
    else:
      form.instance = topic_service.create_topic(obj.topic_name)

  def save_related(self, request, form, formsets, change):
    topic = form.instance
    subtopics_formset = formsets[0]

    save_required = False

    for subtopic in subtopics_formset.save(commit=False):
      if not subtopic.id:
        save_required = True
        topic.associate_subtopic_with_topic(subtopic.subtopic_name, subtopic.category_type, subtopic.subtopic_attrs)

    for subtopic in subtopics_formset.deleted_objects:
      save_required = True
      topic.remove_subtopic(subtopic)

    if save_required:
      topic_service.save_or_update(topic)

  def get_readonly_fields(self, request, obj=None):
    return list(filter(lambda n: n != "topic_name", self.fields or [f.name for f in self.model._meta.fields]))

  def delete_model(self, request, obj):
    topic_service.delete_topic(obj)


admin.site.register(Topic, TopicAdmin)
