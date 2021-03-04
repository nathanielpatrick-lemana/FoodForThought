from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=50)

    def __str__(self):
        return 'item id: {}  item name: {}'.format(self.id, self.name)


class Ingredients(models.Model):
    ingredient = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    restock_level = models.IntegerField()
    unit_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RecipeItem(models.Model):
    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    menu_item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return 'ingredient id: {}  and  menu id: {}'.format(self.ingredient_id, self.menu_item_id)


class Orders(models.Model):
    order = models.IntegerField(primary_key=True)
    order_date = models.DateField()

    def __str__(self):
        return 'order id: {}'.format(self.order)


class CustomerOrders(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    menu_item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return 'order id:{} and menu id: {}'.format(self.order_id, self.menu_item_id)


class ItemStockLevels(models.Model):
    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    restock_date = models.DateField()

    def __str__(self):
        return self.ingredient_id
