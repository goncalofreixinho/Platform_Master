# Generated by Django 3.1.7 on 2023-04-19 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20230419_1609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='input',
            new_name='input_data',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='output',
            new_name='output_data',
        ),
    ]
