# Generated by Django 5.1.4 on 2024-12-21 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0007_submenu_contracts_submenu'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submenu',
            options={'ordering': ('position',), 'verbose_name': 'Операция', 'verbose_name_plural': 'Операции'},
        ),
    ]