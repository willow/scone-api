import reversion

from src.aggregates.client.models import Client, TATopic

reversion.register(Client, follow=['ta_topics'])
reversion.register(TATopic)
