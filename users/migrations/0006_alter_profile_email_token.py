# Generated by Django 5.0.6 on 2025-04-09 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_email_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_token',
            field=models.CharField(default='36cba210-ebc9-482f-a9e2-06ed7a18aead', max_length=100, unique=True),
        ),
    ]
