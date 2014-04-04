lxml: http://stackoverflow.com/a/6504860/173957
This is used for beautifulsoup and scrapy xpath.

  "Since you're on Ubuntu, don't bother with those source packages. Just install those development packages using
  apt-get.

  apt-get install libxml2-dev libxslt-dev
  If you're happy with a possibly older version of lxml altogether though, you could try

  apt-get install python-lxml
  and be done with it. :)"

GEOS: https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/geolibs/#geosbuild
This is used for geo spatial operations.
  "On Debian/Ubuntu, you are advised to install the following packages which will install, directly or by dependency, the required geospatial libraries:

   $ sudo apt-get install binutils libproj-dev gdal-bin"

pyscopg:
  This is in the common.txt becuase one of the packages, django_hstore, depends on postgres. Even if you plan to use
  sqlite for dev purposes, you'll need pscopg installed.

  apt-get install libpq-dev
  apt-get install python-dev
  apt-get install python3-dev OR python3.4-dev OR python3.XXX-dev
