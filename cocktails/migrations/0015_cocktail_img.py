# Generated by Django 5.0 on 2023-12-25 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0014_remove_cocktail_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='cocktail',
            name='img',
            field=models.ImageField(default='media/default.jpg', upload_to='media/'),
        ),
    ]
