# Generated by Django 5.1.1 on 2024-11-11 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile_pic/no-profile.jpg', upload_to='profile_pic/'),
        ),
    ]
