import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView

from . import models as m


class ItemBuyView(View):
    def post(self, _request, id: int, *_args, **_kwargs):
        item: m.Item = get_object_or_404(m.Item, id=id)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": item.currency.value,
                        "product_data": {
                            "name": item.name,
                            "description": item.description,
                            "metadata": {"id": item.pk},
                        },
                        "unit_amount": int(item.price * 100),
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


class OrderBuyView(View):
    def post(self, _request, id: int, *_args, **_kwargs):
        order: m.Order = get_object_or_404(m.Order, id=id)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[  # pyright: ignore
                {
                    "price_data": {
                        "currency": x.item.currency.value,
                        "product_data": {
                            "name": x.item.name,
                            **(
                                {"description": x.item.description}
                                if x.item.description
                                else {}
                            ),
                            "metadata": {"id": order.pk},
                        },
                        "unit_amount": int(x.item.price * 100),
                    },
                    "quantity": x.quantity,
                }
                for x in order.items.all()
            ],
            mode="payment",
            success_url="https://google.com/",
            cancel_url="https://google.com/",
        )

        return redirect(session.url, code=303)  # type: ignore


class OrderDetailView(DetailView):
    queryset = m.Order.objects.prefetch_related("items")
    template_name = "order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["STRIPE_PUBLISHABLE_KEY"] = settings.STRIPE_PUBLISHABLE_KEY
        return context
