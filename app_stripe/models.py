from django.db import models as m


class Currency(m.Model):
    value = m.CharField()

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self) -> str:
        return self.value  # type: ignore


class Item(m.Model):
    name = m.CharField()
    description = m.TextField()
    price = m.DecimalField(max_digits=10, decimal_places=2)
    currency = m.ForeignKey(to="app_stripe.Currency", on_delete=m.PROTECT)

    def __str__(self) -> str:
        return self.name  # type: ignore
