from django.dispatch import receiver
from src.libs.communication_utils.models import Email
from src.libs.communication_utils.services import email_service
from src.libs.communication_utils.signals import email_consumed_by_model


@receiver(email_consumed_by_model, sender=Email)
def email_consumed_by_model_callback(sender, **kwargs):
  email = kwargs['instance']
  associated_model = kwargs['associated_model']
  email_service.associate_model_with_email(email, associated_model)
