from django.db import models, transaction


class AssignedProspect(models.Model):
  client_uid = models.CharField(max_length=100)
  prospect_uid = models.CharField(max_length=100)
  system_created_date = models.DateTimeField()

  class Meta:
    app_label = 'domain'
    unique_together = ("client_uid", "prospect_uid")

  def __str__(self):
    return 'Assigned Prospect #' + str(self.pk)

  def save(self, internal=False, *args, **kwargs):
    if internal:
      with transaction.atomic():
        super().save(*args, **kwargs)
    else:
      from src.apps.domain.engagement_assignment.services import assigned_prospect_service

      assigned_prospect_service.save_or_update(self)
