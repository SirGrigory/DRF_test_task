# Generated by Django 3.2.9 on 2021-11-30 16:13

import clients.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20211121_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='image',
            field=models.ImageField(default='default.png', upload_to=clients.models.upload_to),
        ),
    ]
