from django.dispatch import Signal

email_received = Signal(providing_args=['instance'])
email_consumed_by_model = Signal(providing_args=['instance', 'associated_model'])
