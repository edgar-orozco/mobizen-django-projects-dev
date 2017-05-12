from servicios import models

from rest_framework import serializers

class TelefonosSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Telefono
        fields = ('telnumber',)

class TramitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tramite
        fields = ('name',)

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Servicio
        fields = ('name', 'enabled', 'version')

class DireccionSerializer(serializers.ModelSerializer):
    municipio = serializers.SlugRelatedField(slug_field='name', queryset=models.Municipio.objects.all())
    colonia = serializers.SlugRelatedField(slug_field='name', queryset=models.Colonia.objects.all())
    class Meta:
        model = models.Direccion
        fields = ('calle', 'colonia', 'municipio', 'estado', 'latitud', 'longitud')

class EstablecimientoSerializer(serializers.ModelSerializer):
    telefonos = TelefonosSerializer(many=True, read_only=True)
    tramites = TramitesSerializer(many=True, read_only=True)
    direccion = DireccionSerializer(many=False, read_only=True)
    class Meta:
        model = models.Establecimiento
        fields = ('identificador', 'razon_social', 'tramites', 'telefonos', 'enabled', 'direccion')
