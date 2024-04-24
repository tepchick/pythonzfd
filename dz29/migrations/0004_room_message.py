# Generated by Django 5.0.1 on 2024-01-24 15:16

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0003_alter_product_image_alter_product_qr_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, default='', max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, default='', max_length=300, unique=True, verbose_name='Link')),
            ],
            options={
                'ordering': ('-slug', '-name'),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, default='', verbose_name='Content')),
                ('created', models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, max_length=300, verbose_name='Created')),
                ('user', models.ForeignKey(blank=True, default='', max_length=100, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('room', models.ForeignKey(blank=True, default='', max_length=100, on_delete=django.db.models.deletion.CASCADE, to='django_app.room', verbose_name='Room')),
            ],
            options={
                'ordering': ('-created', '-room'),
            },
        ),
    ]
