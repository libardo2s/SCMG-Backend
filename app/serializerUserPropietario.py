from django.contrib.auth.models import User
from rest_framework import serializers

from .serializerUser import UserSerializer
from .serializerPropietario import PropietarioSerializer


class PropietarioUserSerializer(serializers.ModelSerializer):
    propietario = PropietarioSerializer(many=False)
    usuario = UserSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'propietario', 'usuario')
