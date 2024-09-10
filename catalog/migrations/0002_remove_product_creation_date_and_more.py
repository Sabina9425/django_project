# Generated by Django 5.1.1 on 2024-09-10 17:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="creation_date",
        ),
        migrations.RemoveField(
            model_name="product",
            name="modification_date",
        ),
        migrations.AddField(
            model_name="product",
            name="created_at",
            field=models.DateField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Дата создания продукта",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="updated_at",
            field=models.DateField(
                auto_now=True, verbose_name="Дата изменения продукта"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.TextField(
                help_text="Введите описание категории", max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(
                help_text="Введите описание продукта", max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Загрузите фото продукта",
                null=True,
                upload_to="products/photo",
                verbose_name="Превью",
            ),
        ),
    ]
