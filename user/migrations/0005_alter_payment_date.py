# Generated by Django 5.0.6 on 2024-07-11 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
