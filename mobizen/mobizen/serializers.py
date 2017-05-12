from django.forms import widgets

from drivemee import models
from verifica.models import Client, Vehiculo
from rest_framework import serializers

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Empresa

class OperadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Operador
        fields = ('nombre', 'foto', 'telefono', 'calificacion')

class EvaluacionListSerializer(serializers.ModelSerializer):
    solicitudToken = serializers.ReadOnlyField(source='solicitudToken.deviceToken')
    class Meta:
        model = models.Solicitud
        fields = ('solicitudToken', 'status')

class EvaluacionSerializer(serializers.ModelSerializer):
    deviceToken = serializers.CharField(source='solicitud.client.deviceToken')
    operador = OperadorSerializer(required=False)
    class Meta:
        model = models.Evaluacion
        fields = ('calificacion', 'comentarios', 'no_quiso_calificar', 'operador', 'deviceToken')

class CitaSerializer(serializers.Serializer):
    class Meta:
        model = models.Cita
        fields = ('fecha',)

class DireccionSerializer(serializers.ModelSerializer):
    deviceToken = serializers.CharField(source='solicitud.client.deviceToken')
    calle = serializers.CharField()
    tipo = serializers.CharField()
    class Meta:
        model = models.Direccion
        fields = ('deviceToken', 'calle', 'numero_exterior', 'numero_interior', 'colonia', 'municipio', 'estado', 'codigo_postal', 'latitud', 'longitud', 'tipo', 'referencias')

class DocumentosSerializer(serializers.ModelSerializer):
    deviceToken = serializers.CharField(source='solicitud.client.deviceToken')
    adeudos = serializers.BooleanField(required=True)
    seguro = serializers.BooleanField(required=True)
    tarjeta = serializers.BooleanField(required=True)
    certificado = serializers.BooleanField(required=True)
    enterado = serializers.BooleanField(required=True)
    class Meta:
        model = models.Documento
        fields = ('adeudos','seguro','tarjeta','certificado', 'enterado', 'deviceToken')

class SolicitudNoOperadorSerializer(serializers.ModelSerializer):
    folio = serializers.ReadOnlyField(source='id')
    solicitudToken = serializers.ReadOnlyField(source='solicitudToken.deviceToken')
    direcciones = DireccionSerializer(many=True, read_only=True)
    cita = serializers.ReadOnlyField(source='cita.fecha')
    evaluacion = EvaluacionSerializer(read_only=True)
    cupon = serializers.SlugRelatedField(slug_field='codigo', queryset=models.Cupon.objects.all())
    documentos = DocumentosSerializer(read_only=True)
    class Meta:
        model = models.Solicitud
        fields = ('folio', 'solicitudToken', 'telefono', 'email', 'nombre', 'placa', 'marca', 'submarca', 'modelo','vehiculo', 'cupon', 'direcciones', 'cita', 'evaluacion', 'status', 'documentos', 'ultimo_holograma')

class SolicitudSerializer(serializers.ModelSerializer):
    folio = serializers.ReadOnlyField(source='id')
    solicitudToken = serializers.ReadOnlyField(source='solicitudToken.deviceToken')
    direcciones = DireccionSerializer(many=True, read_only=True)
    operador = OperadorSerializer(read_only=True)
    cita = serializers.ReadOnlyField(source='cita.fecha')
    evaluacion = EvaluacionSerializer(read_only=True)
    cupon = serializers.SlugRelatedField(slug_field='codigo', queryset=models.Cupon.objects.all())
    documentos = DocumentosSerializer(read_only=True)
    class Meta:
        model = models.Solicitud
        fields = ('folio', 'solicitudToken', 'telefono', 'email', 'nombre', 'placa', 'marca', 'submarca', 'modelo','vehiculo', 'cupon', 'direcciones', 'cita', 'operador', 'evaluacion', 'status', 'documentos', 'ultimo_holograma')

class SolicitudInsertSerializer(serializers.Serializer):
    deviceToken = serializers.CharField()
    vehiculo_id = serializers.CharField(required=False)
    telefono = serializers.CharField()
    email = serializers.EmailField()
    nombre = serializers.CharField()
    placa = serializers.CharField()
    marca = serializers.CharField()
    submarca = serializers.CharField()
    modelo = serializers.IntegerField()
    cupon = serializers.CharField(required=False)
    ultimo_holograma = serializers.CharField(required=False)
    coche_registrado = serializers.BooleanField()

class CuponCheckSerializer(serializers.Serializer):
    deviceToken = serializers.CharField()
    codigo = serializers.CharField()
    empresa = serializers.CharField(required=False)

class CuponSerializer(serializers.ModelSerializer):
    empresa = serializers.ReadOnlyField(source='empresa.name')
    class Meta:
        model = models.Cupon
        fields = ('codigo', 'activo', 'descuento', 'empresa')

class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tarifa
        fields = ('estado', 'tipo', 'costo')
