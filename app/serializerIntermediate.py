from rest_framework import serializers

from .models import ComparacionItermediate
from .serializerMarca import MarcaSerializer


class CompareIntermediateSerializer(serializers.ModelSerializer):
    imagen_compare_intermediate = MarcaSerializer(many=False)

    class Meta:
        model = ComparacionItermediate
        fields = ('id', 'imagen_compare_intermediate', 'result_comparation')
