# Generated by Django 5.0 on 2024-01-20 13:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_product_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchase",
            name="purchase_price",
            field=models.DecimalField(decimal_places=2, default=1500, max_digits=10),
            preserve_default=False,
        ),
    ]
