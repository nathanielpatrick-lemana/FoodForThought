from django.db import models


class MenuItems(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    restock_quantity = models.IntegerField()
    restock_date = models.DateField()

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    ingredient = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    restock_quantity = models.IntegerField()

    def __str__(self):
        return self.name


class RecipeItem(models.Model):
    menu_item_id = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.menu_item_id


class Orders(models.Model):
    order = models.IntegerField(primary_key=True)
    order_date = models.DateField()

    def __str__(self):
        return self.order


class CustomerOrders(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    menu_item_id = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.order_id


class ItemStockLevels(models.Model):
    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    restock_date = models.DateField()

    def __str__(self):
        return self.ingredient_id
