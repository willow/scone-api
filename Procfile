web: python manage.py collectstatic --noinput; newrelic-admin run-program gunicorn -c gunicorn.py.ini wsgi:application
# scheduler: python manage.py celery worker -B -E --maxtasksperchild=1000 -- This can be used once we have a bigger
# need for more workers and concurrent schedulers. Remove the '-B' from worker when this is ready as we can only ever
# have one scheduler or we'll have concurrency issues.
worker: python /app/.heroku/python/bin/celery -A src worker -B -E --maxtasksperchild=1000 --loglevel=debug
