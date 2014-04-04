from django.db import models

#according to this url https://code.djangoproject.com/ticket/7835#comment:24
#any model declared in tests.py will be synced. We don't have a tests.py but we do have a tests package
#and test/__init__ is considered the same
class FakeTestClass(models.Model):
  name = models.CharField(max_length=200)
  url = models.URLField()
  trusted_geo_data = models.BooleanField()

  def __unicode__(self):
    return self.name
