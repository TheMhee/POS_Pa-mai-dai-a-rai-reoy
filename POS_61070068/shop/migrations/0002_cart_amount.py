# Generated by Django 3.0.3 on 2020-03-05 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='amount',
            field=models.IntegerField(default=1),
        ),
    ]
