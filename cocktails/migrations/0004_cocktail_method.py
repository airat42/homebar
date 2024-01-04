# Generated by Django 5.0 on 2024-01-04 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0003_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='cocktail',
            name='method',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='cocktails.method'),
            preserve_default=False,
        ),
    ]
