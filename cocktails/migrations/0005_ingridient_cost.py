# Generated by Django 3.2.5 on 2021-09-27 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0004_cocktail_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingridient',
            name='cost',
            field=models.IntegerField(default=100),
        ),
    ]
