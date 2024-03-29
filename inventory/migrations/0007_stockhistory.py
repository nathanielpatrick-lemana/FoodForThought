# Generated by Django 3.1.7 on 2021-04-08 14:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_delete_stockhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockHistory',
            fields=[
                ('date_consumed_stock', models.DateField(default=datetime.date.today)),
                ('stocklevel', models.IntegerField()),
                ('stock_history', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('ingredient_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventory.ingredients')),
            ],
            options={
                'unique_together': {('stock_history', 'ingredient_id')},
            },
        ),
    ]
