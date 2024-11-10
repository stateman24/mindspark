# Generated by Django 5.1.1 on 2024-11-10 14:06

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_profile_options_remove_profile_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(null=True, validators=[django.core.validators.MinValueValidator(limit_value=datetime.date(1924, 12, 5))]),
        ),
    ]