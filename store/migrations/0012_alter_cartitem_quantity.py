# Generated by Django 5.0.6 on 2024-07-13 12:10

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_cartitem_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]
