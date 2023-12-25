# Generated by Django 5.0 on 2023-12-23 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0007_auto_20221023_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingridient_Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=1)),
                ('cocktail_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cocktails.cocktail')),
                ('ingridient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cocktails.ingridient')),
            ],
        ),
    ]
