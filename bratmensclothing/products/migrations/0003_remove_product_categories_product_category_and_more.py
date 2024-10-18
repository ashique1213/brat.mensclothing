# Generated by Django 5.1.2 on 2024-10-18 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_brand_remove_category_brand_name_product_variant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categories',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Tshirt', 'T-shirt'), ('Shirt', 'Shirt'), ('Jeans', 'Jeans'), ('Pants', 'Pants')], default='None', max_length=50),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
