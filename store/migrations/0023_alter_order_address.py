# Generated by Django 5.0.6 on 2024-08-16 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_address_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
