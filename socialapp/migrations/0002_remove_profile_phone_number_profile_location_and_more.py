# Generated by Django 5.0.6 on 2024-06-27 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='blank_profile.jpg', upload_to='profilepic'),
        ),
    ]