from rest_framework import serializers

from .models import Device, DeviceTelemetry, Rack, Sala, TelemetryLog


class DeviceTelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceTelemetry
        fields = '__all__'


class TelemetryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryLog
        fields = '__all__'

    def create(self, validated_data):
        log = super().create(validated_data)
        DeviceTelemetry.objects.update_or_create(
            device=log.device,
            defaults={
                'bateria_pct': log.bateria_pct,
                'status_conexao': log.status_conexao,
                'armazenamento_usado_gb': log.armazenamento_usado_gb,
                'ultimo_log': log.registrado_em,
            },
        )
        return log


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class RackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rack
        fields = '__all__'


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'
