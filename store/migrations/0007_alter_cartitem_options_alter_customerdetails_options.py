# Generated by Django 5.0.6 on 2024-07-11 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_promotions_promotion_alter_address_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Cart Item',
                     'verbose_name_plural': 'Cart Items'},
        ),
        migrations.AlterModelOptions(
            name='customerdetails',
            options={'verbose_name': 'Customer Detail',
                     'verbose_name_plural': 'Customer Details'},
        ),
    ]
