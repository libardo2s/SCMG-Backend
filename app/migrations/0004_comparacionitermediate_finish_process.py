# Generated by Django 2.0.4 on 2018-05-17 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180511_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='comparacionitermediate',
            name='finish_process',
            field=models.BooleanField(default=False),
        ),
    ]