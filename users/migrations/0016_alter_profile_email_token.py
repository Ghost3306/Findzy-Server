# Generated by Django 5.0.6 on 2025-04-13 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_profile_email_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_token',
            field=models.CharField(default='b08a65bb-7f36-4cff-a39b-c8010273ee5d', max_length=100, unique=True),
        ),
    ]
