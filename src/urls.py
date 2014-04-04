from django.contrib import admin
from django.conf.urls import patterns, include, url
from src.apps.rest_api import urls as api_urls

# region Admin Urls
# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns(
  '',
  # Admin panel and documentation:
  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
  url(r'^admin/', include(admin.site.urls)),
)
# endregion

# region Lib Urls

# endregion

# region App Urls
urlpatterns += patterns(
  '',
  url(r'^api/', include(api_urls)),
)
# endregion
