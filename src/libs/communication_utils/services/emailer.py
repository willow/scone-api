import logging
import os
from smtplib import SMTPException
import sendgrid
from django.conf import settings
from src.libs.communication_utils.exceptions import InvalidOutboundEmailError
from src.libs.python_utils.errors.exceptions import re_throw_ex

emailer = sendgrid.SendGridClient(settings.SENDGRID_USERNAME, settings.SENDGRID_PASSWORD, secure=True)

logger = logging.getLogger(__name__)


def send_email(from_address, from_name, to_address, subject, text, html, headers=None):
  msg = sendgrid.Mail(from_address=from_address,from_name=from_name,subject=subject,text=text,html= html)
  msg.add_to(to_address)

  if headers:
    msg.set_headers(headers)

  if settings.DEBUG:
    logger.debug("{sep}******{sep}{0}{sep}{1}{sep}******".format(msg.subject, msg.text, sep=os.linesep))
  else:
    try:
      emailer.send(msg)
    except Exception as e:
      throw_ex = re_throw_ex(SMTPException, "Error sending email", e)

      if "find the recipient domain" in str(e).lower():
        throw_ex = re_throw_ex(InvalidOutboundEmailError, "Invalid email", e)

      raise throw_ex[0](throw_ex[1]).with_traceback(throw_ex[2])
