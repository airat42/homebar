# Generated by Django 5.0 on 2023-12-26 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0016_bill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='cock_name',
            field=models.CharField(max_length=30),
        ),
    ]