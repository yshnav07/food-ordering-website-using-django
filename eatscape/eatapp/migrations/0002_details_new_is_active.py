# Generated by Django 5.1.4 on 2025-01-20 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eatapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='details_new',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]