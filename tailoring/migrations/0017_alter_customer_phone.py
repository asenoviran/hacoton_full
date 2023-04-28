# Generated by Django 4.2 on 2023-04-27 17:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0016_alter_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(validators=[django.core.validators.RegexValidator(message='Invalid phone number', regex='^996?\\d{9}$')]),
        ),
    ]
