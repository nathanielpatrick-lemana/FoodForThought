# Generated by Django 3.1.7 on 2021-04-08 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20210408_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='stock_history',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
    ]
