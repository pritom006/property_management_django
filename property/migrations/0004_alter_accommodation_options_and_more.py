# Generated by Django 5.1.3 on 2025-01-07 07:36

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_accommodationimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accommodation',
            options={'ordering': ['created_at'], 'verbose_name': 'Accommodation', 'verbose_name_plural': 'Accommodations'},
        ),
        migrations.AlterField(
            model_name='accommodation',
            name='images',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=300), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='accommodation',
            name='review_score',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
