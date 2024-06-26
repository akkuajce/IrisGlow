# Generated by Django 4.2.4 on 2024-02-12 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IrisGlowApp', '0003_spects'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('brand_name', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Eyeglasses', 'Eyeglasses'), ('Sunglasses', 'Sunglasses'), ('Computer Glasses', 'Computer Glasses')], max_length=255)),
                ('sub_category', models.CharField(max_length=255)),
                ('product_description', models.TextField()),
                ('material_description', models.TextField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('K', 'Kids')], max_length=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_quantity', models.PositiveIntegerField(default=0)),
                ('production_date', models.DateField(blank=True, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('size', models.CharField(blank=True, max_length=10, null=True)),
                ('frame_material', models.CharField(blank=True, max_length=20, null=True)),
                ('frame_style', models.CharField(blank=True, max_length=20, null=True)),
                ('temple_length', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('bridge_size', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('lens_width', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('thumbnail', models.ImageField(upload_to='frame_thumbnails/')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='frame_images/')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='frame_images/')),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='frame_images/')),
                ('image_5', models.ImageField(blank=True, null=True, upload_to='frame_images/')),
                ('frame_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        
    ]
