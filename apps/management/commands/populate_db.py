from django.core.management.base import BaseCommand
from apps.models import Material, Warehouse, Product, ProductMaterial

class Command(BaseCommand):
    help = "Fills the database with initial data for materials, warehouses, products, and product-material relations"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting database population..."))

        materials = {
            "Mato (paxta)": Material.objects.create(name="Mato (paxta)"),
            "Ip (tikish uchun)": Material.objects.create(name="Ip (tikish uchun)"),
            "Zamok": Material.objects.create(name="Zamok"),
            "Tugma": Material.objects.create(name="Tugma"),
        }

        warehouses = [
            Warehouse.objects.create(material=materials["Mato (paxta)"], remainder=500, price=10000),
            Warehouse.objects.create(material=materials["Ip (tikish uchun)"], remainder=1000, price=5000),
            Warehouse.objects.create(material=materials["Zamok"], remainder=200, price=3000),
            Warehouse.objects.create(material=materials["Tugma"], remainder=1000, price=2000),
        ]

        shirt = Product.objects.create(name="Ko‘ylak", product_code=238923)
        pants = Product.objects.create(name="Shim", product_code=238923)

        ProductMaterial.objects.create(product=shirt, material=materials["Mato (paxta)"], quantity=2)
        ProductMaterial.objects.create(product=shirt, material=materials["Ip (tikish uchun)"], quantity=3)
        ProductMaterial.objects.create(product=shirt, material=materials["Tugma"], quantity=5)

        ProductMaterial.objects.create(product=pants, material=materials["Mato (paxta)"], quantity=3)
        ProductMaterial.objects.create(product=pants, material=materials["Ip (tikish uchun)"], quantity=2)
        ProductMaterial.objects.create(product=pants, material=materials["Zamok"], quantity=1)

        self.stdout.write(self.style.SUCCESS("Database successfully populated! 🚀"))
