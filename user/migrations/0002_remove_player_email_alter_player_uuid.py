# Generated by Django 5.0.6 on 2024-07-11 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='email',
        ),
        migrations.AlterField(
            model_name='player',
            name='uuid',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]
