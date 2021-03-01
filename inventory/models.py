from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    restock_quantity = models.IntegerField()
    restock_date = models.DateField()

    def __str__(self):
        return self.name

# Create your models here.
