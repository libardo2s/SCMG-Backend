# Generated by Django 2.0.4 on 2018-04-15 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComparacionItermediate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_comparation', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ComparacionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen_muestra', models.ImageField(upload_to='usuario', verbose_name='Imagen Usuario')),
                ('fechaDeSubida', models.DateField(auto_now=True)),
                ('result_comparation', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImagenMarcaGanado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='marcas', verbose_name='Imagen Marca')),
                ('imagen_comparacion', models.ImageField(blank=True, null=True, upload_to='comparacion', verbose_name='Imagen Comparacion')),
                ('certificado', models.FileField(blank=True, null=True, upload_to='certificados', verbose_name='Certificado')),
                ('fechaDeSubida', models.DateField(auto_now=True)),
                ('result_comparation', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PropietarioGanado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.IntegerField(unique=True)),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('segundo_nombre', models.CharField(blank=True, max_length=60, null=True, verbose_name='Segundo Nombre')),
                ('apellido', models.CharField(max_length=60, verbose_name='Apellido')),
                ('segundo_apellido', models.CharField(max_length=60, verbose_name='Segundo Apellido')),
                ('ciudad', models.CharField(max_length=80, verbose_name='Ciudad')),
                ('region', models.CharField(max_length=100, verbose_name='Región')),
                ('direccion', models.CharField(max_length=50, verbose_name='Dirección')),
                ('telefono', models.IntegerField(verbose_name='Telefono')),
                ('finca', models.CharField(max_length=80, verbose_name='Finca')),
            ],
        ),
        migrations.AddField(
            model_name='imagenmarcaganado',
            name='propietario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propietario', to='app.PropietarioGanado'),
        ),
        migrations.AddField(
            model_name='comparacionmodel',
            name='imagen_marca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagen_marca', to='app.ImagenMarcaGanado'),
        ),
        migrations.AddField(
            model_name='comparacionitermediate',
            name='imagen_compare_intermediate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imagen_marca_intermediate', to='app.ImagenMarcaGanado'),
        ),
    ]
