import stripe
from django.apps import AppConfig
from django.conf import settings


class StripeConfig(AppConfig):
    name = "app_stripe"

    def ready(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
