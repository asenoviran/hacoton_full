from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from .models import OwnerRequest
from .utils import send_activation_code, create_activation_code

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')
        write_only_fields = ['password']    


    def validate(self, attrs: dict):
        print(attrs)
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают!')
        return attrs
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такая почта уже существует!')
        return email

    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)
        create_activation_code(user)
        send_activation_code(user)
        return user


class ActivationSerializer(serializers.Serializer):
    activation_code = serializers.CharField(max_length=10)

    def validate_activation_code(self, activation_code):
        if User.objects.filter(activation_code=activation_code).exists():
            return activation_code
        raise serializers.ValidationError('Неверно указан код')
    
    def activate(self):
        code = self.validated_data.get('activation_code')
        user = User.objects.get(activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким email не найден')
        return email

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(email=email, password=password, request=request)
            if not user:
                raise serializers.ValidationError('Неправильно указан email или пароль')
            print('User is authenticated:', user)
        else:
            raise serializers.ValidationError('Email и пароль обязательны к заполнению')
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class OwnerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerRequest
        fields = ['message']
