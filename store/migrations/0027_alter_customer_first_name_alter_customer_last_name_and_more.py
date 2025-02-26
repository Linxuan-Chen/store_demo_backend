# Generated by Django 5.1.1 on 2025-01-13 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_remove_collection_featured_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='media/products/'),
        ),
    ]
