from django.db import models
from django.contrib.auth import get_user_model
# from django.core.validators import RegexValidator


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

class OrderTailoring(models.Model):
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
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL,related_name='order_tailorings', null=True, blank=True)
    

    
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
    
    order = models.ForeignKey(OrderTailoring, on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статус заказов'


    def __str__(self):
        return self.status



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

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_products')
    
    class Meta:
        verbose_name = 'Заказ товара'
        verbose_name_plural = 'Заказ товаров'

    def __str__(self):
        return self.product.name
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'product')

    
    def __str__(self):
        return f'Liked by {self.user.email}'
    

    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.product.name} Added to favorites by {self.user.email}'
    

class Review(models.Model):
    product =  models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    def __str__(self) -> str:
        return f'Отзыв от {self.user.email}'
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=50)
    order_tailoring = models.ForeignKey(OrderTailoring, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    order_product = models.ForeignKey(OrderProduct, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f"{self.user.email} ({self.amount})"






