from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Product, Material, ProductMaterial, Warehouse
from .serializers import ProductSerializer, MaterialSerializer, WarehouseSerializer, ProductMaterialSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class ProductMaterialsAPIView(APIView):
    @swagger_auto_schema(request_body=ProductMaterialSerializer)
    def post(self, request):
        serializer = ProductMaterialSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_code = request.data.get("product_code")
        base_quantity = request.data.get("quantity")
        products = Product.objects.filter(product_code=product_code)

        if not products.exists():
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        results = []
        allocated_materials = {}

        for product in products:
            production_qty = base_quantity * product.multiplier if hasattr(product, 'multiplier') else base_quantity

            product_materials = ProductMaterial.objects.filter(product=product)
            warehouse_data = []

            for pm in product_materials:
                material_id = pm.material.id
                required_qty = pm.quantity * production_qty
                material_name = pm.material.name

                warehouses = Warehouse.objects.filter(material_id=material_id).order_by('id')
                total_allocated = 0

                for warehouse in warehouses:
                    already_allocated = allocated_materials.get((material_id, warehouse.id), 0)
                    available_qty = warehouse.remainder - already_allocated
                    if available_qty <= 0:
                        continue

                    if total_allocated < required_qty:
                        qty_to_allocate = min(available_qty, required_qty - total_allocated)
                        total_allocated += qty_to_allocate

                        warehouse_data.append({
                            "warehouse_id": warehouse.id,
                            "material_name": material_name,
                            "qty": qty_to_allocate,
                            "price": warehouse.price
                        })

                        allocated_materials[(material_id, warehouse.id)] = already_allocated + qty_to_allocate

                    if total_allocated >= required_qty:
                        break

                if total_allocated < required_qty:
                    warehouse_data.append({
                        "warehouse_id": None,
                        "material_name": material_name,
                        "qty": required_qty - total_allocated,
                        "price": None
                    })

            results.append({
                "product_name": product.name,
                "product_qty": production_qty,
                "product_materials": warehouse_data
            })

        return Response({"result": results}, status=status.HTTP_200_OK)
