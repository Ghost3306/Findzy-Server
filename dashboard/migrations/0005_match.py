# Generated by Django 5.0.6 on 2025-04-09 18:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_remove_reportitem_location_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('query', models.TextField()),
            ],
        ),
    ]
