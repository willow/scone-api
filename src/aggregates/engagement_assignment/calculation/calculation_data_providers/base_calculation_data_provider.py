from abc import ABC
from src.aggregates.engagement_assignment import constants


class BaseCalculationDataProvider(ABC):
  def provide_calculation_data(self, client, engagement_opportunity):
    ret_val = {}

    ret_val[constants.TA_TOPICS] = [ta_topic.topic_type.topic_name.lower() for ta_topic in client.ta_topics.all()]
    ret_val[constants.STEMMED_TA_TOPICS] = [ta_topic.topic_type.snowball_stem for ta_topic in client.ta_topics.all()]

    return ret_val
