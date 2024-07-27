# Generated by Django 5.0.6 on 2024-06-26 12:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, max_length=50)),
                ('bio', models.TextField(blank=True)),
                ('phone_number', models.IntegerField(blank=True)),
                ('links', models.URLField(blank=True)),
                ('profile_pic', models.ImageField(blank=True, default='', upload_to='profilepic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
