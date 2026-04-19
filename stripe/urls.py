from django.urls import path

from stripe import views as v

urlpatterns = [
    path("buy/<int:id>", v.BuyView.as_view(), name="stripe-buy"),
]
