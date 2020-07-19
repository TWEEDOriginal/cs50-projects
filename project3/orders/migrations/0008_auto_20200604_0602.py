# Generated by Django 3.0.6 on 2020-06-04 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_cartitem_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topping',
            name='dressings',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='toppings',
            field=models.ManyToManyField(blank=True, related_name='carts', to='orders.Topping'),
        ),
    ]
