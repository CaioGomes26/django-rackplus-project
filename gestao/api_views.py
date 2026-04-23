from rest_framework import viewsets
from .models import Sala, Rack, Device, TelemetryLog
from .serializers import SalaSerializer, RackSerializer, DeviceSerializer, TelemetryLogSerializer

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
    queryset = TelemetryLog.objects.all().order_by('-registrado_em')  # Mudar de '-timestamp' para '-registrado_em'
    serializer_class = TelemetryLogSerializer