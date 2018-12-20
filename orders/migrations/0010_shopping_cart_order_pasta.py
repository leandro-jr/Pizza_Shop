# Generated by Django 2.0.3 on 2018-12-14 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_dinner_pasta_salads'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopping_cart',
            name='order_pasta',
            field=models.ManyToManyField(blank=True, related_name='orders_pasta', to='orders.Pasta'),
        ),
    ]
