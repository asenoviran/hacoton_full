# Generated by Django 4.2 on 2023-04-27 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0009_orderstatus_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
