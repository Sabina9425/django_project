import json

from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def handle(self, *args, **options):
        data = self.json_read("catalog.json")

        Product.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        categories = [item for item in data if item['model'] == 'catalog.category']
        products = [item for item in data if item['model'] == 'catalog.product']

        for cat in categories:
            fields = cat['fields']
            category_for_create.append(
                Category(
                    id=cat['pk'],
                    name=fields['name'],
                    description=fields['description']
                )
            )

        Category.objects.bulk_create(category_for_create)

        for prod in products:
            fields = prod['fields']
            category = Category.objects.get(id=fields['category'])
            product_for_create.append(
                Product(
                    id=prod['pk'],
                    name=fields['name'],
                    description=fields['description'],
                    image=fields['image'],
                    category=category,
                    price=fields['price'],
                    created_at=fields['created_at'],
                    updated_at=fields['updated_at']
                )
            )

        Product.objects.bulk_create(product_for_create)
