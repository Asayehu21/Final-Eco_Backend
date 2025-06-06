# Generated by Django 5.1.4 on 2024-12-30 11:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop_app', '0004_rename_madified_at_cart_modified_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(max_length=255, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='ETB', max_length=10)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='myshop_app.cart')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
