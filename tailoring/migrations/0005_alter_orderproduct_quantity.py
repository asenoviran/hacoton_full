# Generated by Django 4.2 on 2023-04-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0004_alter_orderproduct_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]