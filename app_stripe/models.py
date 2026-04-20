from typing import TYPE_CHECKING

from django.db import models as m

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class Currency(m.Model):
    value = m.CharField()

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self) -> str:
        return self.value


class Item(m.Model):
    name = m.CharField()
    description = m.TextField(blank=True)
    price = m.DecimalField(max_digits=10, decimal_places=2)
    currency = m.ForeignKey(Currency, on_delete=m.PROTECT)

    def __str__(self) -> str:
        return f"{self.name}, {self.price}, {self.currency.value}"


class Order(m.Model):
    if TYPE_CHECKING:
        items: "RelatedManager[OrderItem]"

    def __str__(self) -> str:
        return "Order: " + ", ".join(
            f"{x.quantity} x {x.item.name}" for x in self.items.all()
        )


class OrderItem(m.Model):
    order = m.ForeignKey(Order, related_name="items", on_delete=m.PROTECT)
    item = m.ForeignKey(Item, on_delete=m.CASCADE)
    quantity = m.PositiveIntegerField(default=1)
