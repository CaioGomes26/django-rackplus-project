from django.contrib import admin

from .models import Device, DeviceTelemetry, Rack, Sala, TelemetryLog


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'localizacao', 'criado_em']
    search_fields = ['nome', 'localizacao']


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['nome', 'sala', 'criado_em']
    search_fields = ['nome']
    list_filter = ['sala']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['serial_id', 'rack', 'processador', 'ram', 'armazenamento_total_gb', 'criado_em']
    search_fields = ['serial_id', 'processador']
    list_filter = ['rack__sala', 'rack']


@admin.register(DeviceTelemetry)
class DeviceTelemetryAdmin(admin.ModelAdmin):
    list_display = ['device', 'status_conexao', 'bateria_pct', 'armazenamento_usado_gb', 'ultimo_log']
    search_fields = ['device__serial_id']
    list_filter = ['status_conexao', 'device__rack__sala']
    readonly_fields = ['device', 'bateria_pct', 'status_conexao', 'armazenamento_usado_gb', 'ultimo_log', 'atualizado_em']


@admin.register(TelemetryLog)
class TelemetryLogAdmin(admin.ModelAdmin):
    list_display = ['device', 'status_conexao', 'bateria_pct', 'armazenamento_usado_gb', 'registrado_em']
    search_fields = ['device__serial_id']
    list_filter = ['status_conexao']
    readonly_fields = ['device', 'bateria_pct', 'status_conexao', 'armazenamento_usado_gb', 'registrado_em']
