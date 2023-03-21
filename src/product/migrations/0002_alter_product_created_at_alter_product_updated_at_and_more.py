# Generated by Django 4.1.7 on 2023-03-20 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='updated_at',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='updated_at',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='productvariantprice',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='productvariantprice',
            name='updated_at',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='updated_at',
            field=models.TimeField(auto_now=True),
        ),
    ]
