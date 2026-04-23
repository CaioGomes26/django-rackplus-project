from rest_framework import serializers
from .models import Sala, Rack, Device, TelemetryLog

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__' # Serializa todos os campos (armazenamento, bateria, etc)

class RackSerializer(serializers.ModelSerializer):
    # Opcional: Mostra os nomes dos devices dentro do rack no JSON
    devices = DeviceSerializer(many=True, read_only=True, source='device_set')

    class Meta:
        model = Rack
        fields = '__all__'

class SalaSerializer(serializers.ModelSerializer):
    # Opcional: Mostra os racks dentro da sala no JSON
    racks = RackSerializer(many=True, read_only=True, source='rack_set')

    class Meta:
        model = Sala
        fields = '__all__'

class TelemetryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryLog
        fields = '__all__'