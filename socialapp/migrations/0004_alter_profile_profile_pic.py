# Generated by Django 5.0.6 on 2024-06-28 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0003_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='pictures/blank_profile.jpg', upload_to='pictures'),
        ),
    ]
