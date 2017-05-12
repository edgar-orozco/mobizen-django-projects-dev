from django.forms import widgets

from verifica import models

from rest_framework import serializers

###
#
# Reglas HNC
class TerminacionHNCSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Terminacion
        fields = ('value',)

class HologramaHNCSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Holograma
        fields = ('value',)

class SemanaHNCSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Semana
        fields = ('value','title')

class ReglaHNCSerializer(serializers.ModelSerializer):
    terminaciones = TerminacionHNCSerializer(many=True, read_only=True)
    hologramas = HologramaHNCSerializer(many=True, read_only=True)
    semanas = SemanaHNCSerializer(many=True, read_only=True)
    class Meta:
        model = models.ReglaCirculacion
        fields = ('terminaciones','hologramas','semanas')

class DiaHNCSerializer(serializers.ModelSerializer):
    reglas = ReglaHNCSerializer(many=True, read_only=True)
    class Meta:
        model = models.Dia
        fields = ('day_name','value','reglas')

class ProgramaSerializer(serializers.ModelSerializer):
    dias = DiaHNCSerializer(many=True, read_only=True)
    class Meta:
        model = models.Programa
        fields = ('version','title','vigencia_inicio','vigencia_fin','dias',)

class ContingenciaSerializer(serializers.ModelSerializer):
    reglas = ReglaHNCSerializer(many=True, read_only=True)
    class Meta:
        model = models.Contingencia
        fields = ('title','vigencia','reglas',)

# Termina HNC
#
###

class MultaSerializer(serializers.Serializer):
    fundamento = serializers.CharField(required=True)

class InteresseSerializer(serializers.Serializer):
    poliza = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
    motivo = serializers.CharField(required=False)

class CotizacionSerializer(serializers.Serializer):
    idAuto = serializers.CharField()
    cp = serializers.CharField()
    paquete = serializers.CharField()
    plazo = serializers.CharField()
    codColonia = serializers.CharField()
    idCliente = serializers.CharField(required=False)
    valorFactura = serializers.CharField(required=False)
    inicioVigencia = serializers.CharField()
    placa = serializers.CharField(required=False)
    serie = serializers.CharField(required=False)
    telefono = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    nombre = serializers.CharField(required=False)
    deviceToken = serializers.CharField(required=False)
    descripcion = serializers.CharField(required=False)

class CarSerializer(serializers.ModelSerializer):
    marca = serializers.SlugRelatedField(source='manufacturer', slug_field='name', queryset=models.Manufacturer.objects.all())
    submarca = serializers.Field(source='manufacturer.name')
    class Meta:
        model = models.Car
        fields = ('marca', 'submarca')

class VehiculoConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VehiculoConfig
        fields = ('alerta_inicio', 'alerta_mes', 'alerta_quincena', 'alerta_semana', 'alerta_fin')

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppConfig
        fields = ('alertas_hnc', 'alertas_mnc', 'hora_alertas_verificacion', 'hora_alertas_hnc', 'hora_alertas_mnc')
        
class InfraccionesSerializer(serializers.ModelSerializer):
    situacion = serializers.CharField()
    class Meta:
        model = models.Infraccion
        fields = ('folio', 'fecha', 'situacion', 'motivo', 'fundamento', 'short_fundamento', 'sancion')

class VerificacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Verificacion
        fields = ('fecha', 'vigencia', 'resultado')

class TelefonosSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Telefono
        fields = ('title', 'telnumber')

class AseguradorasSerializer(serializers.ModelSerializer):
    telefonos = TelefonosSerializer(many=True, read_only=True)
    class Meta:
        model = models.Aseguradora
        fields = ('id', 'name', 'telefonos')

# class HologramaSerializer(serializers.SlugRelatedField):
#     class Meta:
#         model = models.Holograma

class ClientSerializer(serializers.ModelSerializer):
    deviceToken = serializers.CharField(required=False)
    class Meta:
        model = models.Client
        fields = ('deviceToken', 'deviceToken')

class ClientUpdateSerializer(serializers.ModelSerializer):
    deviceToken = serializers.CharField(required=False)
    build = serializers.IntegerField(required=True)
    version = serializers.CharField(required=True)
    class Meta:
        model = models.Client
        fields = ('deviceToken', 'build', 'version')

class DeviceUpdateSerializer(serializers.ModelSerializer):
    device_os = serializers.CharField(required=True)
    device_os_version = serializers.CharField(required=True)
    push_token = serializers.CharField(required=True)
    onesignal_token = serializers.CharField(required=True)
    device_type = serializers.CharField(required=True)
    deviceToken = serializers.SlugRelatedField(source='client', write_only=True, slug_field='deviceToken', queryset=models.Client.objects.all(), required=False)
    class Meta:
        model = models.DeviceInfo
        fields = ('device_os', 'device_os_version', 'push_token', 'onesignal_token', 'device_type', 'id', 'deviceToken')

class SeguroSerializer(serializers.ModelSerializer):
    aseguradora = serializers.SlugRelatedField(slug_field='name', queryset=models.Aseguradora.objects.all())
    cobertura = serializers.SlugRelatedField(slug_field='valor_interesse', queryset=models.Paquete.objects.all())
    class Meta:
        model = models.Seguro
        fields = ('poliza', 'vigencia', 'titular', 'aseguradora', 'activo', 'boughtInApp', 'cobertura')

class SeguroUpdateSerializer(serializers.Serializer):
    titular = serializers.CharField(required=False, allow_null=True)
    aseguradora = serializers.CharField()
    poliza = serializers.CharField(required=False)
    vigencia = serializers.DateField()
    activo = serializers.BooleanField(required=False)
    boughtInApp = serializers.BooleanField(required=False)
    cobertura = serializers.IntegerField(required=False)
    class Meta:
        fields = ('poliza', 'vigencia', 'titular', 'aseguradora', 'activo', 'boughtInApp', 'cobertura')
    def get_validation_exclusions(self):
        exclusions = super(SeguroUpdateSerializer, self).get_validation_exclusions()
        return exclusions + ['titular', 'boughtInApp', 'cobertura']

class VehiculoSerializer(serializers.ModelSerializer):
#     holograma = serializers.SlugRelatedField(many=False, read_only=False, slug_field='name')
    infracciones = InfraccionesSerializer(many=True, read_only=True)
    verificacion = VerificacionesSerializer(many=True, read_only=True)
    tenencias = serializers.SlugRelatedField(many=True, slug_field='periodo', read_only=True)
    deviceToken = serializers.SlugRelatedField(source='client', write_only=True, slug_field='deviceToken', queryset=models.Client.objects.all())
    seguro = SeguroSerializer(many=True, required=False, read_only=True)
    marca = serializers.ReadOnlyField(source='car.manufacturer.name')
    submarca = serializers.ReadOnlyField(source='car.name')
    class Meta:
        model = models.Vehiculo
        fields = ('id', 'deviceToken', 'alias', 'placa', 'modelo', 'vin', 'tarjeta_circulacion_permanente', 'tarjeta_circulacion_vigencia', 'codigo_postal', 'query_string', 'exento', 'infracciones', 'verificacion', 'tenencias', 'seguro',  'marca', 'submarca', 'image', 'last_update')

class VehiculoUpdateSerializer(serializers.ModelSerializer):
    alias = serializers.CharField(required=False)
    placa = serializers.CharField(required=False)
    modelo = serializers.CharField(required=False)
#     marca = serializers.CharField(source='car.manufacturer.name', required=False)
#     submarca = serializers.CharField(source='car.name', required=False)
    class Meta:
        model = models.Vehiculo
        fields = ('alias', 'placa', 'modelo', 'vin', 'tarjeta_circulacion_permanente', 'tarjeta_circulacion_vigencia', 'codigo_postal', 'query_string', 'exento')

class VehiculoConsultaSerializer(serializers.ModelSerializer):
    placa = serializers.CharField(required=True)
#     marca = serializers.CharField(source='car.manufacturer.name', required=False)
#     submarca = serializers.CharField(source='car.name', required=False)
    class Meta:
        model = models.Vehiculo
        fields = ('placa')

class ReleaseNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReleaseNotes
        fields = ('title', 'body', 'button', 'actionTarget', 'actionType')

class BuildsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Builds
        fields = ('number', 'number')

class AppVersionSerializer(serializers.ModelSerializer):
    notas = ReleaseNotesSerializer(many=True, read_only=True)
    builds = BuildsSerializer(many=True, read_only=True)
    class Meta:
        model = models.AppVersion
        fields = ('version', 'builds', 'notas')

class BuildNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BuildNote
        fields = ('title', 'body', 'button', 'actionTarget', 'actionType')

class BuildSerializer(serializers.ModelSerializer):
    notas = BuildNoteSerializer(many=True, read_only=True)
    class Meta:
        model = models.Builds
        fields = ('number', 'notas')

class PaqueteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='valor_interesse')
    nombre = serializers.ReadOnlyField()
    class Meta:
        model = models.Paquete
        fields = ('nombre', 'id')

class PlazoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='valor_interesse')
    nombre = serializers.ReadOnlyField()
    class Meta:
        model = models.Plazo
        fields = ('nombre', 'id')

class ImecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Imeca
        fields = ('imecas', 'particula', 'hora', 'fecha', 'indice_uv')

class CotizadorErrorSerializer(serializers.ModelSerializer):
    descripcion = serializers.CharField(required=True)
    class Meta:
        model = models.CotizadorError
        fields = ('descripcion', 'descripcion')

class ReciboSerializer(serializers.ModelSerializer):
    poliza = serializers.CharField(required=True)
    class Meta:
        model = models.Recibo
        fields = ('poliza', 'poliza')

class CotizadorSerializer(serializers.ModelSerializer):
    deviceToken = serializers.CharField(required=True)
    paquete = serializers.IntegerField(required=True)
    plazo = serializers.IntegerField(required=True)
    fecha = serializers.DateField(required=True)
    costo = serializers.CharField(required=True)
    coche_registrado = serializers.BooleanField(required=True)
    aseguradora = serializers.CharField(required=True)
    class Meta:
        model = models.Cotizacion
        fields = ('deviceToken', 'paquete', 'plazo', 'fecha', 'costo', 'coche_registrado', 'aseguradora')

class TarifaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TarifaItem
        fields = ('order', 'name', 'costo')

class TarifaSerializer(serializers.ModelSerializer):
    items = TarifaItemSerializer(many=True)
    salario_minimo = serializers.SlugRelatedField(slug_field='valor', queryset=models.SalarioMinimo.objects.all())
    class Meta:
        model = models.Tarifa
        fields = ('estado', 'footer', 'salario_minimo', 'items')

class PagoTenenciaSerializer(serializers.Serializer):
    tenencia = serializers.CharField(required=True)
    deviceToken = serializers.CharField(required=True)

class PagoInfraccionSerializer(serializers.Serializer):
    folio_infraccion = serializers.CharField(required=True)
    deviceToken = serializers.CharField(required=True)

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class SubscriptionSerializer(serializers.ModelSerializer):
    expiration_time = serializers.DateTimeField(required=True)
    sub_source = serializers.CharField(required=True, write_only=True)
    gps_token = serializers.CharField(required=False, write_only=True)
    gps_subscriptionId = serializers.CharField(required=False, write_only=True)
    gps_packageName = serializers.CharField(required=False, write_only=True)
    ios_receipt = serializers.CharField(required=False, write_only=True)
    autoRenewing = serializers.BooleanField(required=False, write_only=True)
    expiryTimeMillis = serializers.IntegerField(required=False, write_only=True)
    startTimeMillis = serializers.IntegerField(required=False, write_only=True)
    class Meta:
        model = models.Subscription
        fields = ('expiration_time', 'sub_source', 'gps_token', 'gps_subscriptionId', 'gps_packageName', 'ios_receipt', 'autoRenewing', 'expiryTimeMillis', 'startTimeMillis')

class PlacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoPlaca
        fields = ('tipo', 'estado')
