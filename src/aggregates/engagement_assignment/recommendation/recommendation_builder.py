from src.aggregates.engagement_assignment.recommendation import clause_service


class RecommendationBuilder:
  def __init__(self, recommendation_data, _clause_service=clause_service):
    self.recommendation_data = recommendation_data
    self._ta_name_clause = None
    self._target_action_clause = None
    self._about_clause = None
    self.response_clause = None

    self._clause_service = _clause_service

  def _set_ta_name_clause(self):
    self._ta_name_clause = self._clause_service.get_ta_name_clause(self.recommendation_data)

  def _set_ta_action_clause(self):
    self._target_action_clause = self._clause_service.get_ta_action_clause(self.recommendation_data)

  def _set_about_clause(self):
    self._about_clause = self._clause_service.get_about_clause(self.recommendation_data)

  def _set_response_clause(self):
    self.response_clause = self._clause_service.get_response_clause(self.recommendation_data)

  def build_recommended_action(self):
    self._set_ta_name_clause()
    self._set_ta_action_clause()
    self._set_about_clause()
    self._set_response_clause()

    return " ".join((self._ta_name_clause, self._target_action_clause, self._about_clause, self.response_clause))
