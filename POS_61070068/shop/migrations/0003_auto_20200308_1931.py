# Generated by Django 3.0.3 on 2020-03-08 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_cart_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='description',
            field=models.CharField(default='', max_length=300),
        ),
    ]
