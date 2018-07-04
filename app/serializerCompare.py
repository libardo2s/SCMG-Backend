from rest_framework import serializers
from .models import ComparacionModel
from .serializerMarca import MarcaSerializer


class CompareSerializer(serializers.ModelSerializer):
    imagen_marca = MarcaSerializer(many=False)

    class Meta:
        model = ComparacionModel
        fields = ('id', 'imagen_marca', 'imagen_muestra', 'fechaDeSubida', 'result_comparation')
