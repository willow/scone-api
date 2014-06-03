from django.contrib import admin

from src.aggregates.engagement_assignment.models import EngagementAssignment, Recommendation


class RecommendationInline(admin.TabularInline):
  model = Recommendation
  readonly_fields = ('recommended_action',)
  can_delete = False


class EngagementAssignmentAdmin(admin.ModelAdmin):
  actions = None
  ordering = ('-score',)
  list_filter = ('client',)

  inlines = [
    RecommendationInline,
  ]

  def engagement_opportunity_attrs(self, ea):
    return ea.engagement_opportunity.engagement_opportunity_attrs

  def pre_score(self, ea):
    return ea.score_attrs['pre_score']

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
    return (self.fields or [f.name for f in self.model._meta.fields]) + ['engagement_opportunity_attrs', 'pre_score']


admin.site.register(EngagementAssignment, EngagementAssignmentAdmin)
