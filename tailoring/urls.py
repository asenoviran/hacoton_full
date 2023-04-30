from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import  OrderProductViewSet, OrderViewSet, ProductCategoryViewSet, ProductViewSet, FavoriteListAPIView


router = DefaultRouter()
router.register('orderproduct', OrderProductViewSet, 'orderproducts')
router.register('order', OrderViewSet, 'orders')
router.register('productcategory', ProductCategoryViewSet, 'productcategorys')
router.register('product', ProductViewSet, 'products')


urlpatterns = [
    path('', include(router.urls)),
    path('favorites/', FavoriteListAPIView.as_view(), name='favorites'),
    
]
