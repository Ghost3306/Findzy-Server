# Generated by Django 5.0.6 on 2025-04-13 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_profile_email_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_token',
            field=models.CharField(default='32885312-b38f-4f7f-9c69-0addb4d9cedd', max_length=100, unique=True),
        ),
    ]
