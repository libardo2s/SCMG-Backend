from rest_framework import serializers

from .serializerPropietario import PropietarioSerializer
from .models import ImagenMarcaGanado


class MarcaSerializer(serializers.ModelSerializer):
    propietario = PropietarioSerializer(many=False)

    class Meta:
        model = ImagenMarcaGanado
        fields = ('id', 'propietario', 'imagen', 'fechaDeSubida', 'result_comparation')
