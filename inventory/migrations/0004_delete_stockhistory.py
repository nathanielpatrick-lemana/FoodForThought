# Generated by Django 3.1.7 on 2021-04-08 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_stockhistory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StockHistory',
        ),
    ]
