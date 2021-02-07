# Generated by Django 3.1.5 on 2021-02-07 17:56

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_remove_map_users_who_played'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='map',
            name='locations',
        ),
        migrations.AddField(
            model_name='map',
            name='mapillary_image_key',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=25), default=['NOKEYASSIGNED'], size=None),
            preserve_default=False,
        ),
    ]
