# Generated by Django 3.1.5 on 2021-02-15 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20210215_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='players',
            name='guessed_trigger',
            field=models.BooleanField(default=False),
        ),
    ]
