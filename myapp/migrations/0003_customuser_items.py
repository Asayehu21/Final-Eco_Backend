# Generated by Django 5.1.4 on 2025-01-05 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_customuser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='items',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
