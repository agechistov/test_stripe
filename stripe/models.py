from django.db import models as m


class Item(m.Model):
    name = m.TextField()
    description = m.TextField()
    price = m.DecimalField(max_digits=10, decimal_places=2)
