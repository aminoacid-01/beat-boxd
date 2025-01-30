# Generated by Django 4.2.18 on 2025-01-30 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_review_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='status',
            field=models.IntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=0),
        ),
    ]
