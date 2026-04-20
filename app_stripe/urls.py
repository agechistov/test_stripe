from django.urls import path

from . import views as v

urlpatterns = [
    path("buy/<int:id>", v.ItemBuyView.as_view(), name="stripe-item-buy"),
    path("item/<int:pk>", v.ItemDetailView.as_view(), name="stripe-item-detail"),
]
