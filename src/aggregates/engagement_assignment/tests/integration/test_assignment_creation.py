import pytest
from src.aggregates.engagement_assignment.services import engagement_assignment_tasks


def test_refresh_engagement_assignments():
  assert True


def test_linkedin_score():
  engagement_assignment_tasks.refresh_assignments_task.delay()
  assert True
