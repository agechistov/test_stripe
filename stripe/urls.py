from django.urls import path

from stripe import views as v

urlpatterns = [
    path("buy/<int:id>", v.ItemBuyView.as_view(), name="stripe-item-buy"),
]
