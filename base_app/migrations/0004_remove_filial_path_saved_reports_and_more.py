# Generated by Django 5.1.4 on 2024-12-19 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0003_remove_contracts_path_saved_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filial',
            name='path_saved_reports',
        ),
        migrations.AlterField(
            model_name='filial',
            name='path_saved_order',
            field=models.CharField(max_length=255, verbose_name='Сетевая папка филиала'),
        ),
    ]
