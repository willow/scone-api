from django.db import models
from reversion.models import Revision


class RevisionEvent(models.Model):
  revision  = models.ForeignKey(Revision)
  version = models.PositiveIntegerField()
  name = models.CharField(max_length=1024)
  data = models.TextField()
