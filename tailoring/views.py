from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, render
from rest_framework import filters, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Avg, Count
from rest_framework.response import Response
from django.http import HttpResponse
from .permissions import IsAuthor, IsOwnerAndAuthor, IsOwner
from .serializers import OrderSerializer, OrderStatusSerializer, OrderProductSerializer, ProductCategorySerializer, ProductSerializer, FavoriteSerializer, LikeSerializer, ReviewSerializer
from .models import Order, OrderStatus, OrderProduct, Product, ProductCategory, Review, Favorite, Like

from django.core.mail import send_mail
from django.conf import settings


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    # queryset = OrderStatus.objects.all()
    serializer_class = OrderSerializer

    # def send_email(self, *args, **kwargs):
    #     status = kwargs.get('status')
    #     # def send_order_status_email(order):
    #     subject = f"Заказ {order.pk} изменен на статус {order.status}"
    #     message = f"Уважаемый(-ая) {order.customer.first_name},\n\nСтатус вашего заказа изменен на {order.status}."
    #     from_email = settings.EMAIL_HOST_USER
    #     recipient_list = [order.customer.email]

    #     send_mail(subject, message, from_email, recipient_list)

    def update_order_status(self, request, order_status_id):
        order_status = OrderStatus.objects.get(id=order_status_id)
        order_status.status
        order_status.save()

        # отправляем сообщение на почту заказчику
        order = order_status.orders
        subject = 'Ваш заказ готов'
        message = f'Заказ {order} готов к выдаче.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email]
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse('Статус заказа успешно обновлен и отправлено уведомление на почту заказчику')

class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]


    def get_permissions(self):
        if self.action == self.action == 'like' or self.action == 'favorite' or self.action == 'review':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            self.permission_classes = [IsOwner]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsOwnerAndAuthor]
        return super().get_permissions()
        

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    

    def get_serializer_class(self):
        if  self.action == 'like':
            return LikeSerializer
        elif self.action == 'favorite':
            return FavoriteSerializer
        elif self.action == 'review':
            return ReviewSerializer
        return super().get_serializer_class()
    

    @action(methods=['POST', 'DELETE'], detail=True)
    def review(self, request, pk=None):
        product = self.get_object()
        if request.method == 'POST':
            serializer = ReviewSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, product=product)
            return Response(serializer.data)
        if request.method == 'DELETE':
            review = get_object_or_404(Review.objects.filter(id=pk))
            if request.user != review.user:
                return Response({'error': 'Нельзя удалить чужой отзыв'}, status=403)
            review.delete()
            return Response({'message': 'Ваш отзыв удален'})
    

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        product = self.get_object()
        like = Like.objects.filter(user=request.user, product=product)
        if like.exists():
            like.delete()
            liked = False
        else:
            Like.objects.create(user=request.user, product=product)
            liked = True
        likes_count = Like.objects.filter(product=product).count()
        response_data = {'liked': liked, 'likes_count': likes_count}
        return Response(response_data)
    

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        product = self.get_object()
        favor = Favorite.objects.filter(user=request.user, product=product)
        if favor.exists():
            favor.delete()
            favor = False
        else:
            Favorite.objects.create(user=request.user, product=product)
            favor = True

        return Response({'In Favorite': favor})
    


class OrderProductViewSet(ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer


class FavoriteListAPIView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context