# Generated by Django 4.2 on 2023-05-01 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0026_rename_order_payment_order_tailoring_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderstatus',
            old_name='orders',
            new_name='order',
        ),
    ]
