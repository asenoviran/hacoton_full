from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsAuthor
from .serializers import OrderSerializer, OrderStatusSerializer, OrderProductSerializer, ProductCategorySerializer, ProductSerializer, EmployeeSerializer, DocumentSerializer
from .models import Order, OrderStatus, OrderProduct, Product, ProductCategory, Document, Employee




class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        Возвращает текущий статус заказа
        """
        order = self.get_object()
        status_serializer = OrderStatusSerializer(order.status)
        return Response(status_serializer.data)

    def perform_create(self, serializer):
        """
        Добавление заказа и установка статуса "В обработке"
        """
        order = serializer.save()
        OrderStatus.objects.create(order=order, status='В обработке')

    def perform_update(self, serializer):
        """
        Обновление заказа и установка нового статуса
        """
        order = serializer.save()
        status = self.request.data.get('status')
        if status:
            OrderStatus.objects.create(order=order, status=status)

class OrderStatusViewSet(ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderProductViewSet(ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer