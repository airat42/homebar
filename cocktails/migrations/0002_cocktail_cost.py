# Generated by Django 3.2.5 on 2021-08-12 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cocktail',
            name='cost',
            field=models.IntegerField(default=1),
        ),
    ]
