# Generated by Django 5.0.6 on 2024-07-17 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdetails',
            name='customer_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_details', to='store.customer'),
        ),
    ]
