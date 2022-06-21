from django.db import models


class Store(models.Model):
    name = models.CharField(" ", max_length=64)


class Purchase(models.Model):
    store = models.ForeignKey(Store, verbose_name="", on_delete=models.CASCADE)
    name = models.CharField(" ", max_length=128, db_column="product")
    price = models.DecimalField(", .", max_digits=10, decimal_places=2)
