from django.dispatch import Signal

engagement_opportunity_discovered = Signal(providing_args=['engagement_opportunity_discovery_object'])
