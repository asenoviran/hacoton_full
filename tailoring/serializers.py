from rest_framework import serializers
from .models import Order, OrderStatus, Employee, Document, ProductCategory, Product, OrderProduct



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
    status = OrderStatusSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        employee = Employee.objects.create(**validated_data)
        return employee


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.file = validated_data.get('file', instance.file)
        instance.save()
        return instance


class ProductCategorySerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0.")
        return value


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше 0.")
        return value
