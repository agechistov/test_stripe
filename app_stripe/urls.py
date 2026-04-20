from django.urls import path

from . import views as v

urlpatterns = [
    path("buy/item/<int:id>", v.ItemBuyView.as_view(), name="stripe-item-buy"),
    path("buy/order/<int:id>", v.OrderBuyView.as_view(), name="stripe-order-buy"),
    path("item/<int:pk>", v.ItemDetailView.as_view(), name="stripe-item-detail"),
    path("order/<int:pk>", v.OrderDetailView.as_view(), name="stripe-order-detail"),
]
