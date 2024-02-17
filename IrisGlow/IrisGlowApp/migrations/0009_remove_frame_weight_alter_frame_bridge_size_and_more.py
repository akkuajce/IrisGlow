# Generated by Django 4.2.4 on 2024-02-13 05:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IrisGlowApp', '0008_alter_frame_color_alter_frame_frame_material_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='frame',
            name='weight',
        ),
        migrations.AlterField(
            model_name='frame',
            name='bridge_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(15), django.core.validators.MaxValueValidator(25)]),
        ),
        migrations.AlterField(
            model_name='frame',
            name='lens_width',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(45), django.core.validators.MaxValueValidator(58)]),
        ),
        migrations.AlterField(
            model_name='frame',
            name='temple_length',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(140), django.core.validators.MaxValueValidator(155)]),
        ),
    ]