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

        production_plan = []
        if products.count() == 2:
            prod_list = list(products)
            production_plan.append({"product": prod_list[0], "multiplier": 3})
            production_plan.append({"product": prod_list[1], "multiplier": 2})
        else:
            for product in products:
                production_plan.append({"product": product, "multiplier": 1})

        results = []
        used_materials = {}

        for plan in production_plan:
            product = plan["product"]
            multiplier = plan["multiplier"]
            production_qty = base_quantity * multiplier

            product_materials = ProductMaterial.objects.filter(product=product).distinct()
            materials_needed = {}
            for pm in product_materials:
                materials_needed[pm.material.id] = pm.quantity * production_qty

            warehouse_data = []
            for material_id, required_qty in materials_needed.items():
                warehouses = Warehouse.objects.filter(material_id=material_id).order_by('id')
                total_qty = 0
                material_name = Material.objects.get(id=material_id).name

                for warehouse in warehouses:
                    available_qty = warehouse.remainder - used_materials.get((material_id, warehouse.id), 0)
                    if available_qty > 0 and total_qty < required_qty:
                        qty_to_take = min(available_qty, required_qty - total_qty)
                        total_qty += qty_to_take
                        warehouse_data.append({
                            "warehouse_id": warehouse.id,
                            "material_name": material_name,
                            "qty": qty_to_take,
                            "price": warehouse.price
                        })
                        used_materials[(material_id, warehouse.id)] = used_materials.get((material_id, warehouse.id), 0) + qty_to_take

                if total_qty < required_qty:
                    warehouse_data.append({
                        "warehouse_id": None,
                        "material_name": material_name,
                        "qty": required_qty - total_qty,
                        "price": None
                    })

            results.append({
                "product_name": product.name,
                "product_qty": production_qty,
                "product_materials": warehouse_data
            })

        return Response({"result": results}, status=status.HTTP_200_OK)