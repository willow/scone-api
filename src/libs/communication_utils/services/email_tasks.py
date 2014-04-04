import logging
from smtplib import SMTPException
from celery.exceptions import Ignore
from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.utils import encoding
from src.libs.communication_utils.exceptions import InvalidOutboundEmailError
from src.libs.communication_utils.services import email_service
from src.libs.python_utils.errors.exceptions import log_ex_with_message

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def send_email_task(self, from_address, from_name, to_address, subject, plain_text_body,
                    associated_model_content_type_app, associated_model_content_type_model, associated_model_id):
  associated_model_type = ContentType.objects.get(
    app_label=associated_model_content_type_app, model=associated_model_content_type_model
  )

  associated_model = associated_model_type.get_object_for_this_type(pk=associated_model_id)

  try:
    email_service.send_email(from_address, from_name, to_address, subject, plain_text_body, associated_model)
  except InvalidOutboundEmailError:
    raise Ignore()
  except SMTPException as e:
    logger.warn(log_ex_with_message("SMTP Error sending email", e))
    raise self.retry(exc=e)


@shared_task(bind=True)
def reply_to_email_task(self, email_id, plain_text_body, associated_model_content_type_app,
                        associated_model_content_type_model,
                        associated_model_id, **kwargs):

  associated_model_type = ContentType.objects.get(
    app_label=associated_model_content_type_app, model=associated_model_content_type_model
  )

  email = email_service.get_email(email_id)

  associated_model = associated_model_type.get_object_for_this_type(pk=associated_model_id)

  try:
    email_service.reply_to_email(email, plain_text_body, associated_model, **kwargs)
    print(('reply email run email from: subject %s' % encoding.smart_unicode((self.request.id,
                                                                                   email.from_address),
                                                                                 errors='ignore')))
  except InvalidOutboundEmailError as e:
    logger.warn(log_ex_with_message("Invalid outbound", e))
    raise Ignore()
  except SMTPException as e:
    logger.warn(log_ex_with_message("SMTP Error replying to email", e))
    raise self.retry(exc=e)
