from django.db import models
from jsonfield import JSONField
from src.libs.django_utils.serialization.flexible_json_serializer import JSONSerializer


class Event(models.Model):
  version = models.PositiveIntegerField()
  name = models.CharField(max_length=1024)
  data = JSONField(load_kwargs={'cls': JSONSerializer})

  def __str__(self):
    return 'Event #' + str(self.pk) + ': ' + self.name
