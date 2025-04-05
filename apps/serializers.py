from rest_framework import serializers
from .models import Product, Material, ProductMaterial, Warehouse

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'product_code']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id','name']

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id','material', 'remainder', 'price']


class ProductMaterialSerializer(serializers.ModelSerializer):
    product_code = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_code(self, value):
        if not Product.objects.filter(product_code=value).exists():
            raise serializers.ValidationError("Product not found.")
        return value

    def validate(self, data):
        return data

    class Meta:
        model = ProductMaterial
        fields = ['product_code', 'quantity']
