# Generated by Django 4.1.13 on 2023-12-01 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ramdeals', '0002_carts_productscarts'),
    ]

    operations = [
        migrations.AddField(
            model_name='carts',
            name='isFinished',
            field=models.BooleanField(default=False),
        ),
    ]
