# Generated by Django 5.0.6 on 2025-02-04 09:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phoneapp', '0004_extendeduser'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumber',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
