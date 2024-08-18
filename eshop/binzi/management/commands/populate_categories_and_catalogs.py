from django.core.management.base import BaseCommand
from models import Category, Catalog

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        categories = [
            'Electronics', 'Clothing', 'Home & Kitchen', 'Books',
            'Beauty & Personal Care', 'Toys & Games', 'Sports & Outdoors',
            'Food & Beverages', 'Automotive', 'Furniture'
        ]
        catalogs = [
            'Digital clothing catalog', 'Grocery store online catalog',
            'Book retailer\'s catalog', 'Furniture catalog'
        ]

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)

        for catalog_name in catalogs:
            Catalog.objects.get_or_create(name=catalog_name)

        self.stdout.write(self.style.SUCCESS('Successfully populated categories and catalogs'))