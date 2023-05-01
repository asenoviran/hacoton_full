from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import  OrderProductViewSet, OrderTailoringViewSet, ProductCategoryViewSet, ProductViewSet, FavoriteListAPIView, PaymentViewSet


router = DefaultRouter()
router.register('orderproduct', OrderProductViewSet, 'orderproduct')
router.register('ordertailoring', OrderTailoringViewSet, 'ordertailoring')
router.register('productcategory', ProductCategoryViewSet, 'productcategory')
router.register('product', ProductViewSet, 'products')
router.register('payment', PaymentViewSet, 'payments')



urlpatterns = [
    path('', include(router.urls)),
    path('favorites/', FavoriteListAPIView.as_view(), name='favorites'),
    
]
