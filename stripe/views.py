from django.conf import settings
from django.views.generic import DetailView
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

import stripe

from . import models as m

stripe.api_key = settings.STRIPE_SECRET_KEY  # type: ignore


class BuySerializer(serializers.Serializer):
    session_id = serializers.CharField()


class ItemBuyView(GenericAPIView):
    serializer_class = BuySerializer
    queryset = m.Item.objects.all()  # type: ignore
    lookup_field = "id"

    def get(self, _request, *_args, **_kwargs):
        instance: m.Item = self.get_object()
        session = stripe.checkout.Session.create(  # type: ignore
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": instance.name,
                            "description ": instance.description,
                            "metadata": {"id": instance.id},
                        },
                        "unit_amount_decimal": str(instance.price),
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
        )
        return Response(self.get_serializer({"session_id": session.id}).data)


class ItemDetailView(DetailView):
    model = m.Item
    template_name = "item_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["STRIPE_PUBLISHABLE_KEY"] = settings.STRIPE_PUBLISHABLE_KEY
        return context
