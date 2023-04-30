from rest_framework import serializers
from .models import Order, OrderStatus, ProductCategory, Product, OrderProduct, Like, Review, Favorite



class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'

        def validate(self, data):
        # проверка, что заказчик имеет телефон или email
            if not data.get('customer').phone and not data.get('customer').email:
                raise serializers.ValidationError("Необходимо указать телефон или email заказчика.")
        
        # проверка, что товар активен
            if not data.get('product').is_active:
                raise serializers.ValidationError("Выбранный товар неактивен.")
        

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'



class ProductCategorySerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(method_name='get_likes_count')
    image = serializers.ImageField(max_length=None, use_url=True)
    

    class Meta:
        model = Product
        fields = '__all__'

    
    def get_likes_count(self, instance) -> int:
        return Like.objects.filter(product=instance).count()
    

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['liked_users'] = LikeSerializer(instance.likes.all(), many=True).data
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        return representation
    



class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше 0.")
        return value
    
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    
    class Meta:
        model = Like
        fields = ('user',)


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Favorite
        fields = ('user', 'product')



class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'user', 'product', 'text', 'created_at', 'updated_at')
        read_only_fields = ['product']
