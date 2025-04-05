from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, MaterialViewSet, ProductMaterialsAPIView, WarehouseViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')

urlpatterns = [
    path('', include(router.urls)),
    path('product-materials/', ProductMaterialsAPIView.as_view(), name='product-materials-detail'),
]