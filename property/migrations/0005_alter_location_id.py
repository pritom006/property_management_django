# Generated by Django 5.1.3 on 2025-01-07 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_alter_accommodation_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
