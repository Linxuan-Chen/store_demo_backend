# Generated by Django 5.0.6 on 2024-08-16 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_customer_first_name_alter_customer_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdetails',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='phone',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
