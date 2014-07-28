from django.contrib import admin

from src.libs.common_domain.models import Event


class EventAdmin(admin.ModelAdmin):
  actions = None



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
    return (self.fields or [f.name for f in self.model._meta.fields])

admin.site.register(Event, EventAdmin)
