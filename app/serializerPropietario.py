from rest_framework import serializers
from .models import PropietarioGanado


class PropietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropietarioGanado
        fields = '__all__'
