# Generated by Django 5.1 on 2024-08-16 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binzi', '0009_catalog_category_product_catalog_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalog',
            name='description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.AlterField(
            model_name='catalog',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
