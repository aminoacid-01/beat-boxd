# Generated by Django 4.2.18 on 2025-01-31 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_album_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
