# Generated by Django 5.0 on 2024-01-19 20:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_alter_review_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="quantity",
            field=models.IntegerField(default=10, max_length=10),
            preserve_default=False,
        ),
    ]
