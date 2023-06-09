# Generated by Django 4.2 on 2023-05-01 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tailoring', '0024_remove_orderstatus_customuser_orderproduct_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTailoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('product_type', models.CharField(choices=[('shirt', 'Рубашка'), ('pants', 'Брюки'), ('dress', 'Платье')], max_length=10)),
                ('size', models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L')], max_length=1)),
                ('color', models.CharField(choices=[('red', 'Красный'), ('blue', 'Синий'), ('green', 'Зеленый'), ('black', 'Черный'), ('white', 'Белый')], max_length=10)),
                ('material', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заказ на пошив',
                'verbose_name_plural': 'Заказы на пошивы',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_charge_id', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='tailoring.ordertailoring')),
                ('order_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tailoring.orderproduct')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
        migrations.AddField(
            model_name='ordertailoring',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_tailorings', to='tailoring.payment'),
        ),
        migrations.AddField(
            model_name='product',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tailoring.payment'),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='orders',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tailoring.ordertailoring'),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
