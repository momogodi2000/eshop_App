# Generated by Django 5.1 on 2024-08-18 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binzi', '0020_contact_delete_faq_remove_order_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usersetting', to=settings.AUTH_USER_MODEL),
        ),
    ]
