from rest_framework.routers import DefaultRouter
from .views import  OrderProductViewSet, OrderStatusViewSet, OrderViewSet, ProductCategoryViewSet, ProductViewSet, EmployeeViewSet, DocumentViewSet

router = DefaultRouter()
router.register('orderproduct', OrderProductViewSet, 'orderproducts')
router.register('orderstatus', OrderStatusViewSet, 'orderstatus')
router.register('order', OrderViewSet, 'orders')
router.register('productcategory', ProductCategoryViewSet, 'productcategorys')
router.register('product', ProductViewSet, 'products')
router.register('employe', EmployeeViewSet, 'employes')
router.register('document', DocumentViewSet, 'documents')
urlpatterns = router.urls
