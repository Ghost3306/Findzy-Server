# Generated by Django 5.0.6 on 2025-04-13 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_profile_email_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_token',
            field=models.CharField(default='6b09c20b-e5d9-425f-be0a-44b5c21e6e20', max_length=100, unique=True),
        ),
    ]
