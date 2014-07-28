from celery import shared_task
import logging
import time

log = logging.getLogger(__name__)

@shared_task
def test_task(message="Hellow World!", kwargs=None):
  if not kwargs: kwargs = {}
  log.warn("BEGIN" + message)
  time.sleep(7)
  log.warn("END" + message)
