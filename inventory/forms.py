from django import forms


class OrderForm(forms.Form):
    # order_this = forms.BooleanField(help_text="Do you want to order this item?", required=False, initial=False)
    item_quantity = forms.IntegerField(help_text="Order how many?", min_value=0, initial=0, required=False)


class IngredientForm(forms.Form):
    name = forms.CharField(help_text="Ingredient name")
    quantity = forms.IntegerField(help_text="Amount ordered or currently in stock", initial=0)
