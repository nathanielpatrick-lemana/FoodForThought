# Generated by Django 3.1.7 on 2021-04-08 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20210408_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='ingredient_id',
            field=models.IntegerField(default=1),
        ),
    ]