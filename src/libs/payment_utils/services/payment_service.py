from django.conf import settings
import stripe
from src.libs.payment_utils.exceptions import ChargeError, InvalidCardError
from src.libs.python_utils.errors.exceptions import re_throw_ex


def charge_payment(amount_in_dollars, token, description):
  stripe.api_key = settings.STRIPE_SECRET_KEY
  amount_in_cents = int(amount_in_dollars * 100)

  try:
    charge = stripe.Charge.create(
      amount=amount_in_cents,
      currency="usd",
      card=token,
      description=description
    )
  except stripe.CardError as e:
    throw_ex = re_throw_ex(ChargeError, "Error processing payment", e)

    if "security code is incorrect" in str(e).lower():
      throw_ex = re_throw_ex(InvalidCardError, "Invalid card", e)

    raise throw_ex[0](throw_ex[1]).with_traceback(throw_ex[2])

  return charge
