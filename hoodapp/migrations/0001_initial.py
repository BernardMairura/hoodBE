# Generated by Django 3.1.4 on 2020-12-05 12:41

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('bio', models.TextField(blank=True, max_length=100)),
                ('prof_picture', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('contact', models.CharField(blank=True, max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(max_length=60)),
                ('hoodphoto', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('body', models.TextField(blank=True, max_length=100)),
                ('resident_count', models.IntegerField(blank=True, null=True)),
                ('emergency_contact', models.IntegerField(blank=True, null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoodapp.adminprofile')),
            ],
            options={
                'db_table': 'neighborhood',
            },
        ),
        migrations.CreateModel(
            name='SuperuserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('bio', models.TextField(blank=True, max_length=100)),
                ('prof_picture', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('contact', models.CharField(blank=True, max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OccupantProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('bio', models.TextField(blank=True, max_length=100)),
                ('prof_picture', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('contact', models.CharField(blank=True, max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('hoodname', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home', to='hoodapp.neighborhood')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField(blank=True, max_length=100)),
                ('location', models.CharField(max_length=60)),
                ('hood_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business', to='hoodapp.neighborhood')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='neighbor_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
