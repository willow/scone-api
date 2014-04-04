import logging
from django.utils import encoding
from src.libs.communication_utils.services import email_tasks

logger = logging.getLogger(__name__)


def send_email(from_address, from_name, to_address, subject, plain_text_body, associated_model, eta=None):
  associated_model_content_type_app = associated_model._meta.app_label
  associated_model_content_type_model = associated_model._meta.verbose_name
  associated_model_content_type_id = associated_model.pk

  email_tasks.send_email_task.apply_async(
    (
      from_address, from_name, to_address, subject, plain_text_body,
      associated_model_content_type_app, associated_model_content_type_model,
      associated_model_content_type_id,
    ),
    eta=eta
  )


def reply_to_email(email, plain_text_body, associated_model, eta=None, **kwargs):
  associated_model_content_type_app = associated_model._meta.app_label
  associated_model_content_type_model = associated_model._meta.verbose_name
  associated_model_content_type_id = associated_model.pk

  async_result = email_tasks.reply_to_email_task.apply_async(
    (
      email.pk, plain_text_body,
      associated_model_content_type_app, associated_model_content_type_model,
      associated_model_content_type_id,
    ),
    kwargs=kwargs,
    eta=eta
  )

  print(('reply email send email from: %s' % encoding.smart_unicode((async_result.id, email.from_address),
                                                                        errors='ignore')))
