# Generated by Django 4.0.4 on 2022-06-10 15:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('django_app', '0002_alter_product_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
