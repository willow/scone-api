from django.core.management.base import CommandError, BaseCommand
from src.libs.common_domain import event_store


class Command(BaseCommand):
  def handle(self, *args, **options):
    try:
      event_name = args[0]
    except:
      raise CommandError('Missing event name')

    event_store.replay_events(event_name)
