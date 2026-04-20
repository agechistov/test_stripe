from django.db import models as m


class Item(m.Model):
    name = m.CharField()
    description = m.TextField()
    price = m.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name  # type: ignore
