# Generated by Django 3.1.4 on 2020-12-05 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hoodapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='hood_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hoodapp.neighborhood'),
        ),
        migrations.AlterField(
            model_name='business',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
