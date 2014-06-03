from django.utils import timezone
from unittest.mock import MagicMock
from src.libs.communication_utils.models import Email
from src.libs.communication_utils.tests.email_test_data import email_1


def test_email_model_sets_message_id():
  email = Email.construct_incoming_email(**email_1)
  assert email.message_id == '<11471247.33986.1361999987364.JavaMail.root@vms170015>'


def test_email_model_sets_reply_message_id():
  reply_message = '<20130916040724.5.38922.c45993@d4dab1f6-91ca-43a6-8ced-4d8a340e7403.prvt.dyno.rt.heroku.com>'
  in_reply_to = 'In-Reply-To: %s\r\n' % reply_message

  email = Email.construct_incoming_email(**dict(email_1, **{'headers': email_1['headers'] + in_reply_to}))
  assert email.in_reply_to_message_id == reply_message


def test_email_model_sets_date():
  some_date = timezone.now()

  datetime_parser = MagicMock()
  datetime_parser.get_datetime = MagicMock(return_value=some_date)

  email = Email.construct_incoming_email(_datetime_parser=datetime_parser, **email_1)

  assert email.sent_date == some_date


def test_email_model_sets_direction():
  email = Email.construct_incoming_email(**email_1)
  assert email.email_direction == Email.email_direction_incoming


def test_email_model_corrects_from_keyword():
  from_address = 'something@test.com'
  email = Email.construct_incoming_email(**dict(email_1, **{'from': from_address}))
  assert email.from_address == from_address


def test_email_model_corrects_attachment():
  email_dict = dict(email_1, **{'attachments': 1})
  Email.construct_incoming_email(**email_dict)

def test_email_model_validates():
  email_dict = dict(email_1, **{'dkim': 'none','SPF':'pass'})
  Email.construct_incoming_email(**email_dict)

def test_email_model_validates_unknown_kwargs():
  email_dict = dict(email_1, **{'content-ids': 'none', 'attachment-info': 'none'})
  Email.construct_incoming_email(**email_dict)

