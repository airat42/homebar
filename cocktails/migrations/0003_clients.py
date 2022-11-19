# Generated by Django 3.2.5 on 2021-08-12 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0002_cocktail_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('balance', models.IntegerField(default=0)),
            ],
        ),
    ]
