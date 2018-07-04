# Generated by Django 2.0.4 on 2018-04-16 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioPropietario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propietario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_propietario', to='app.PropietarioGanado')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_propietario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
