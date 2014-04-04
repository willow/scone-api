from email import utils
from email.utils import parseaddr
import logging
import os
from django.conf import settings
from email_reply_parser import EmailReplyParser
from src.libs.communication_utils.models import Email
from src.libs.communication_utils.services import emailer
from src.libs.communication_utils.signals import email_received

logger = logging.getLogger(__name__)


def is_spam(**kwargs):
  ret_val = False

  spam_score = kwargs.get('spam_score')

  try:

    spam_value = float(spam_score)

    if spam_value >= settings.SPAM_SCORE_THRESHOLD:
      ret_val = True

  except (ValueError, TypeError):
    pass

  return ret_val


def save_or_update(email):
  email.full_clean()
  email.save(internal=True)

  return email


def get_email(email_id):
  return Email.objects.get(pk=email_id)


def create_incoming_mail(email):
  save_or_update(email)
  email_received.send(Email, instance=email)

  return email


def get_reply_contents(email):
  return EmailReplyParser.parse_reply(email.text)


def associate_model_with_email(email, associated_model):
  email.associate_model(associated_model)
  save_or_update(email)


def send_email(from_address, from_name, to_address, subject, plain_text_body, associated_model):
  html_body = convert_text_to_html(plain_text_body)
  formatted_from_address = utils.formataddr((from_name, from_address))

  emailer.send_email(from_address, from_name, to_address, subject, plain_text_body, html_body)

  email_model = Email(
    email_direction=Email.email_direction_outgoing,
    text=plain_text_body,
    html=html_body,
    from_address=formatted_from_address,
    to=to_address,
    subject=subject
  )

  save_or_update(email_model)

  associate_model_with_email(email_model, associated_model)

  logger.debug("Email sent: {0}".format(email_model))


def reply_to_email(email, plain_text_body, associated_model, **kwargs):
  html_body = convert_text_to_html(plain_text_body)

  # if they pass in *just* an email address with no name, then we don't really need to do anything
  # but if they pass in "My Name" <someguy@test.com> then we need just the email address.
  from_address = parseaddr(kwargs.get('from_address', email.from_address))[1]
  from_name = kwargs.get('from_name')

  formatted_from_address = utils.formataddr((from_name, from_address))

  in_reply_to = email.message_id
  #references is not a field we store in the db, but it helps for delivery.
  references = email.message_id
  headers = {'In-Reply-To': in_reply_to, 'References': references}

  subject = "Re: " + email.subject

  to_address = email.from_address

  emailer.send_email(from_address, from_name, to_address, subject, plain_text_body, html_body, headers)

  email_model = Email(
    email_direction=Email.email_direction_outgoing,
    text=plain_text_body,
    html=html_body,
    from_address=formatted_from_address,
    to=to_address,
    subject=subject,
    in_reply_to_message_id=in_reply_to
  )

  save_or_update(email_model)

  associate_model_with_email(email_model, associated_model)

  logger.debug("Email replied: {0}".format(email_model))


def convert_text_to_html(text):
  html_body = text.replace(os.linesep, '<br/>')
  return html_body
