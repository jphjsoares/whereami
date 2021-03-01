# Generated by Django 3.1.5 on 2021-01-30 21:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('creator', models.CharField(max_length=40)),
                ('create_date', models.DateField(auto_now=True)),
                ('num_of_locations', models.IntegerField(default=0)),
                ('locations', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None), size=None)),
                ('times_played', models.IntegerField(default=0)),
            ],
        ),
    ]
