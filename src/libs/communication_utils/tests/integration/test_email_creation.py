from django.core.exceptions import ValidationError
import pytest
from src.libs.communication_utils.models import Email
from src.libs.communication_utils.services import email_service
from src.libs.communication_utils.tests.email_test_data import email_1


@pytest.mark.django_db_with_migrations
def test_email_is_created_from_attrs():
  email = Email.construct_incoming_email(**email_1)

  email_id = email_service.save_or_update(email).id

  email_aggregate = Email.objects.get(pk=email_id)

  assert 1 == Email.objects.count()


@pytest.mark.django_db_with_migrations
def test_email_fails_with_high_spam():
  with pytest.raises(ValidationError):
    email = Email.construct_incoming_email(**dict(email_1, **{'spam_score': 10}))

    email_id = email_service.save_or_update(email).id
