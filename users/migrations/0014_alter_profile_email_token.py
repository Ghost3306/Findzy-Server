# Generated by Django 5.0.6 on 2025-04-13 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_profile_email_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_token',
            field=models.CharField(default='2ad352c9-71d5-492b-a1ae-83d42ad65f70', max_length=100, unique=True),
        ),
    ]
