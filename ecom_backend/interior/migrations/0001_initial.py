# Generated by Django 4.2.8 on 2024-10-04 12:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DesignCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Design Category',
                'verbose_name_plural': 'Design Categories',
                'db_table': 'design_categories',
            },
        ),
        migrations.CreateModel(
            name='InteriorDesignProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='interior.designcategory')),
            ],
            options={
                'verbose_name': 'Interior Design Project',
                'verbose_name_plural': 'Interior Design Projects',
                'db_table': 'interior_design_projects',
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Room Type',
                'verbose_name_plural': 'Room Types',
                'db_table': 'room_types',
            },
        ),
        migrations.CreateModel(
            name='ServicePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('features', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Service Package',
                'verbose_name_plural': 'Service Packages',
                'db_table': 'service_packages',
            },
        ),
        migrations.CreateModel(
            name='InteriorRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('dimensions', models.CharField(blank=True, max_length=100, null=True)),
                ('design_description', models.TextField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='interior.interiordesignproject')),
                ('room_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rooms', to='interior.roomtype')),
            ],
            options={
                'verbose_name': 'Interior Room',
                'verbose_name_plural': 'Interior Rooms',
                'db_table': 'interior_rooms',
            },
        ),
        migrations.CreateModel(
            name='DesignImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='design_images/')),
                ('description', models.TextField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='interior.interiordesignproject')),
            ],
            options={
                'verbose_name': 'Design Image',
                'verbose_name_plural': 'Design Images',
                'db_table': 'design_images',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('booking_date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed')], max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='customer.customer')),
                ('project', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking', to='interior.interiordesignproject')),
                ('service_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='interior.servicepackage')),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
                'db_table': 'bookings',
            },
        ),
    ]
