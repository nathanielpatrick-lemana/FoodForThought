# Generated by Django 3.1.7 on 2021-03-29 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_stockhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='paid',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='total',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]