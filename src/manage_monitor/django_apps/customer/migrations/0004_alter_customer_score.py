# Generated by Django 4.2.2 on 2023-07-03 16:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_customer_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='score',
            field=models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
