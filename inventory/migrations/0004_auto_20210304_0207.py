# Generated by Django 3.1.7 on 2021-03-04 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_itemstocklevels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorders',
            name='menu_item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item'),
        ),
        migrations.AlterField(
            model_name='recipeitem',
            name='menu_item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item'),
        ),
        migrations.DeleteModel(
            name='MenuItems',
        ),
    ]
