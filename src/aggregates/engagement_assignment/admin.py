from django.contrib import admin
from src.aggregates.engagement_assignment import constants

from src.aggregates.engagement_assignment.models import EngagementAssignment, Recommendation
from src.aggregates.engagement_opportunity.services import engagement_opportunity_service
from src.aggregates.profile.services import profile_service
from src.aggregates.topic.models import Topic
from src.aggregates.topic.services import topic_service
from src.apps.graph.engagement_assignment.services.engagement_assignment_graph_service import \
  get_assignments_from_topic_type


class RecommendationInline(admin.TabularInline):
  model = Recommendation
  readonly_fields = ('recommended_action',)
  can_delete = False


class EntityTypeFilter(admin.SimpleListFilter):
  title = "entity type"
  parameter_name = 'entity_type'

  def lookups(self, request, model_admin):
    return (
      (constants.ASSIGNED_EO_UIDS, 'engagement opportunity'),
      (constants.ASSIGNED_PROFILE_UIDS, 'profile'),
    )

  def queryset(self, request, queryset):
    if self.value() == constants.ASSIGNED_EO_UIDS:
      return queryset.filter(assignment_attrs__contains=constants.ASSIGNED_EO_UIDS)

    elif self.value() == constants.ASSIGNED_PROFILE_UIDS:
      return queryset.filter(assignment_attrs__contains=constants.ASSIGNED_PROFILE_UIDS)


class TopicTypeFilter(admin.SimpleListFilter):
  title = "topic type"
  parameter_name = 'topic_type'

  def lookups(self, request, model_admin):
    return Topic.objects.all().values_list("id", "topic_name")

  def queryset(self, request, queryset):
    topic_id = self.value()

    if topic_id:

      topic = topic_service.get_topic(topic_id)
      topic_uid = topic.topic_uid
      ea_uids = get_assignments_from_topic_type(topic_uid)

      return queryset.filter(engagement_assignment_uid__in=ea_uids)


class EngagementAssignmentAdmin(admin.ModelAdmin):
  actions = None
  ordering = ('-score',)
  list_filter = ('client', EntityTypeFilter, TopicTypeFilter)

  inlines = [
    RecommendationInline,
  ]

  def entity_attrs(self, ea):
    ret_val = []

    for attr, vals in ea.assignment_attrs.items():

      if attr == constants.ASSIGNED_EO_UIDS:
        for eo_id in vals:
          eo = engagement_opportunity_service.get_engagement_opportunity(eo_id)
          ret_val.append(eo.engagement_opportunity_attrs)

      elif attr == constants.ASSIGNED_PROFILE_UIDS:
        for profile_id in vals:
          profile = profile_service.get_profile(profile_id)
          ret_val.append(profile.profile_attrs)

    return ret_val

  def pre_score(self, ea):
    pre_score = 0
    for score in ea.score_attrs:
      pre_score += score['score_attrs']['pre_score']

    return pre_score

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
    return (self.fields or [f.name for f in self.model._meta.fields]) + ['entity_attrs', 'pre_score']


admin.site.register(EngagementAssignment, EngagementAssignmentAdmin)
