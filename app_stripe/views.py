import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView

from . import models as m


class ItemBuyView(View):
    def post(self, _request, id: int, *_args, **_kwargs):
        instance: m.Item = get_object_or_404(m.Item, id=id)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": instance.currency.value,
                        "product_data": {
                            "name": instance.name,
                            "description": instance.description,
                            "metadata": {"id": instance.pk},
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

        return redirect(session.url, code=303)  # type: ignore


class ItemDetailView(DetailView):
    queryset = m.Item.objects.select_related("currency")
    template_name = "item_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["STRIPE_PUBLISHABLE_KEY"] = settings.STRIPE_PUBLISHABLE_KEY
        return context
