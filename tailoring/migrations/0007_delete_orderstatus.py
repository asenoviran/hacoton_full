# Generated by Django 4.2 on 2023-04-27 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0006_alter_order_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderStatus',
        ),
    ]