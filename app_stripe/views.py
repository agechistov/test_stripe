import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import DetailView
from rest_framework.generics import GenericAPIView

from . import models as m


class ItemBuyView(GenericAPIView):
    queryset = m.Item.objects.all()  # type: ignore
    lookup_field = "id"

    def post(self, _request, *_args, **_kwargs):
        instance: m.Item = self.get_object()
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": instance.name,
                            "description": instance.description,
                            "metadata": {"id": instance.id},
                        },
                        "unit_amount": int(instance.price * 100),
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url="https://google.com/",
            cancel_url="https://google.com/",
        )
        return redirect(session.url, code=303)


class ItemDetailView(DetailView):
    model = m.Item
    template_name = "item_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["STRIPE_PUBLISHABLE_KEY"] = settings.STRIPE_PUBLISHABLE_KEY
        return context
