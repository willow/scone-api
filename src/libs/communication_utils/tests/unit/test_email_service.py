import pytest
from src.libs.communication_utils.services import email_service


@pytest.mark.parametrize(("input_values", "expected"), [
  ({'spam_score': 2.3}, True),
  ({'spam_score': 4}, True),
  ({'spam_score': 1}, False),
  ({'something_else': 4}, False),
  ({'something_else': 4, 'spam_score': 6}, True),
])
def test_email_service_detects_spam(input_values, expected):
  assert expected == email_service.is_spam(**input_values)
