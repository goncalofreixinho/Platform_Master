# Generated by Django 3.1.7 on 2023-04-18 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_feedback_star_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='star_rating',
        ),
        migrations.AddField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
