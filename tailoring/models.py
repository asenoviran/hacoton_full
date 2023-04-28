from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator


User = get_user_model()

# class Customer(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone_regex = RegexValidator(regex=r'^996?\d{9}$', message='Invalid phone number')
#     phone = models.CharField(validators=[phone_regex])

#     class Meta:
#         verbose_name = 'Клиент'
#         verbose_name_plural = 'Клиенты'

#     def __str__(self):
#         return self.name

class Order(models.Model):
    TYPE_CHOICES = (
        ('shirt', 'Рубашка'),
        ('pants', 'Брюки'),
        ('dress', 'Платье'),
    )

    SIZE_CHOICES = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
    )

    COLOR_CHOICES = (
        ('red', 'Красный'),
        ('blue', 'Синий'),
        ('green', 'Зеленый'),
        ('black', 'Черный'),
        ('white', 'Белый'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    product_type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    size = models.CharField(choices=SIZE_CHOICES, max_length=1)
    color = models.CharField(choices=COLOR_CHOICES, max_length=10)
    material = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    

    
    class Meta:
        verbose_name = 'Заказ на пошив'
        verbose_name_plural = 'Заказы на пошивы'

    def __str__(self):
        return f"{self.product_type} ({self.size}, {self.color})"



class OrderStatus(models.Model):
    STATUS_CHOICES = (
        ('processing', 'В обработке'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен'),
    )

    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статус заказов'
        

    def __str__(self):
        return self.status
    


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class Document(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='documents/')
    
    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return f"{self.document_type} for Order {self.order}"



class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


    def __str__(self):
        return self.name
    

class Product(models.Model):
    SIZE_CHOICES = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
    )

    COLOR_CHOICES = (
        ('red', 'Красный'),
        ('blue', 'Синий'),
        ('green', 'Зеленый'),
        ('black', 'Черный'),
        ('white', 'Белый'),
    )

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=50)
    size = models.CharField(choices=SIZE_CHOICES, max_length=1)
    color = models.CharField(choices=COLOR_CHOICES, max_length=10)
    material = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


    def __str__(self):
        return self.name

class OrderProduct(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    
    class Meta:
        verbose_name = 'Заказ товара'
        verbose_name_plural = 'Заказ товаров'

    def __str__(self):
        return self.product.name
    






