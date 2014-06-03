import reversion

from src.aggregates.topic.models import Topic, Subtopic


reversion.register(Topic, follow=['subtopics'])
reversion.register(Subtopic)
