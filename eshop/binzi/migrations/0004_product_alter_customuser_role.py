# Generated by Django 5.1 on 2024-08-15 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binzi', '0003_contactmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('max_quantity', models.IntegerField()),
                ('min_quantity', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/image/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('in_stock', 'In Stock'), ('full_stock', 'Full Stock'), ('stock_alert', 'Stock Alert')], default='in_stock', max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('deliver', 'Deliver'), ('client', 'Client')], default='client', max_length=30),
        ),
    ]
