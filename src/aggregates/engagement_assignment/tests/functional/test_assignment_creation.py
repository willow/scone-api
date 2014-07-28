import pytest
from src.aggregates.engagement_assignment.services import engagement_assignment_tasks


@pytest.mark.django_db()
@pytest.mark.graph_db
@pytest.mark.load_fixture(fixture_name="test_ea_data_reddit_twitter_eo.json")
@pytest.mark.replay_events
def test_refresh_engagement_assignments():
  assert True

@pytest.mark.django_db()
@pytest.mark.graph_db
@pytest.mark.load_fixture(fixture_name="test_ea_data_linkedin_profile.json")
@pytest.mark.replay_events
def test_linkedin_score():
  engagement_assignment_tasks.refresh_assignments_task.delay()
  assert True
