from src.aggregates.engagement_assignment.calculation import score_processor
from src.aggregates.engagement_assignment.tests.ea_test_data import assignment_1


def test_score_processor_returns_correct_total_for_prospect_base_attrs():
  ret_val = score_processor.process_score(assignment_1)


