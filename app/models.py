import sys
from PIL import Image
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


class PropietarioGanado(models.Model):
    documento = models.IntegerField(unique=True)
    nombre = models.CharField('Nombre', max_length=50)
    segundo_nombre = models.CharField('Segundo Nombre', max_length=60, blank=True, null=True)
    apellido = models.CharField('Apellido', max_length=60)
    segundo_apellido = models.CharField('Segundo Apellido', max_length=60)
    ciudad = models.CharField('Ciudad', max_length=80)
    region = models.CharField('Región', max_length=100)
    direccion = models.CharField('Dirección', max_length=50)
    telefono = models.CharField('Telefono', max_length=10)
    finca = models.CharField('Finca', max_length=80)
    activo = models.BooleanField('Activo', default=True)

    def __str__(self):
        return '%s %s' % (self.nombre, self.apellido)


class ImagenMarcaGanado(models.Model):
    propietario = models.ForeignKey(PropietarioGanado, related_name='propietario', on_delete=models.CASCADE)
    imagen = models.ImageField('Imagen Marca', upload_to='marcas')
    imagen_comparacion = models.ImageField('Imagen Comparacion', upload_to='comparacion', blank=True, null=True)
    certificado = models.FileField('Certificado', upload_to='certificados', blank=True, null=True)
    fechaDeSubida = models.DateField(auto_now=True)
    result_comparation = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.propietario.nombre, self.propietario.apellido)

    def save(self, *args, **kwargs):
        if self.imagen_comparacion:
            # Opening the uploaded image
            im = Image.open(self.imagen_comparacion)

            output = BytesIO()

            # Resize/modify the image
            im = im.resize((512, 512))

            # after modifications, save it to the output
            im.save(output, format='JPEG', quality=100)
            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            self.imagen_comparacion = InMemoryUploadedFile(
                output,
                'ImageField', "%s.jpg" % self.imagen_comparacion.name.split('.')[0], 'image/jpeg',
                sys.getsizeof(output), None)

        super(ImagenMarcaGanado, self).save(*args, **kwargs)


class ComparacionModel(models.Model):
    imagen_marca = models.ForeignKey(ImagenMarcaGanado, related_name='imagen_marca', on_delete=models.CASCADE)
    imagen_muestra = models.ImageField('Imagen Usuario', upload_to='usuario')
    fechaDeSubida = models.DateField(auto_now=True)
    result_comparation = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.imagen_marca.propietario.nombre, self.imagen_marca.propietario.apellido)

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        im = Image.open(self.imagen_muestra)

        output = BytesIO()

        # Resize/modify the image
        im = im.resize((512, 512))

        # after modifications, save it to the output
        im.save(output, format='JPEG', quality=100)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.imagen_muestra = InMemoryUploadedFile(
            output,
            'ImageField', "%s.jpg" % self.imagen_muestra.name.split('.')[0], 'image/jpeg',
            sys.getsizeof(output), None)

        super(ComparacionModel, self).save(*args, **kwargs)


class ComparacionItermediate(models.Model):
    imagen_compare_intermediate = models.ForeignKey(
        ImagenMarcaGanado,
        related_name='imagen_marca_intermediate',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    result_comparation = models.FloatField(blank=True, null=True)
    finish_process = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class UsuarioPropietario(models.Model):
    propietario = models.OneToOneField(PropietarioGanado, related_name='usuario_propietario', on_delete=models.CASCADE)
    usuario = models.OneToOneField(User, related_name='usuario_propietario', on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.propietario.nombre, self.propietario.apellido)
