# Generated by Django 4.2.18 on 2025-02-01 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_comment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='album',
            unique_together={('title', 'artist')},
        ),
    ]
