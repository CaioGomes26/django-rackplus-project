from rest_framework import viewsets

from .models import Device, Rack, Sala, TelemetryLog
from .serializers import DeviceSerializer, RackSerializer, SalaSerializer, TelemetryLogSerializer


class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer


class RackViewSet(viewsets.ModelViewSet):
    queryset = Rack.objects.all()
    serializer_class = RackSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class TelemetryLogViewSet(viewsets.ModelViewSet):
    queryset = TelemetryLog.objects.select_related('device').order_by('-registrado_em')
    serializer_class = TelemetryLogSerializer
