# Generated by Django 4.2 on 2023-05-01 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0025_ordertailoring_payment_ordertailoring_payment_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='order',
            new_name='order_tailoring',
        ),
        migrations.RemoveField(
            model_name='product',
            name='payment',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_products', to='tailoring.payment'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='tailoring.orderproduct'),
        ),
    ]
