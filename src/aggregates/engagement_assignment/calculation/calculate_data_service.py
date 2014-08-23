from src.aggregates.engagement_assignment import constants

from src.aggregates.engagement_opportunity.models import EngagementOpportunity
from src.aggregates.profile.models import Profile
from src.aggregates.topic.enums import TopicCategoryEnum


def provide_stemmed_keywords(client, assigned_entities):
  ret_val = []

  for assigned_entity in assigned_entities:

    if isinstance(assigned_entity, Profile):
      profile = assigned_entity
      profile_attrs = profile.profile_attrs
      topic_ids = profile_attrs.get(constants.TOPIC_IDS)

    elif isinstance(assigned_entity, EngagementOpportunity):
      eo = assigned_entity
      topic_ids = list(eo.topics.values_list('topic_type_id', flat=True))

    else:
      raise Exception("Invalid assigned type")

    for ta_topic in client.ta_topics.exclude(topic_type_id__in=topic_ids):

      # store the `root` topic's stemmed value
      ret_val.append(ta_topic.topic_type.snowball_stem)

      # now iterate through each of the sub topics and get their stem too
      for keywords_topic in ta_topic.topic_type.subtopics.filter(category_type=TopicCategoryEnum.keywords):
        ret_val.append(keywords_topic.subtopic_attrs[constants.SNOWBALL_STEM])

  return list(set(ret_val))
