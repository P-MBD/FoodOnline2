# Generated by Django 4.1.7 on 2023-03-25 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0004_alter_vendor_vendor_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendor",
            name="vendor_slug",
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
