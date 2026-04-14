from django.contrib import admin

from .models import Device, Rack, Sala, TelemetryLog


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'localizacao', 'criado_em']
    search_fields = ['nome', 'localizacao']


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['nome', 'sala', 'criado_em']
    search_fields = ['nome']
    list_filter = ['sala']  # filtro lateral por sala


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['serial_id', 'rack', 'status_conexao', 'bateria_pct', 'ultimo_log']
    search_fields = ['serial_id']
    list_filter = ['status_conexao', 'rack__sala']  # filtra por status e por sala do rack


@admin.register(TelemetryLog)
class TelemetryLogAdmin(admin.ModelAdmin):
    list_display = ['device', 'status_conexao', 'bateria_pct', 'armazenamento_usado_gb', 'registrado_em']
    search_fields = ['device__serial_id']
    list_filter = ['status_conexao']
    readonly_fields = ['device', 'bateria_pct', 'status_conexao', 'armazenamento_usado_gb', 'registrado_em']  # log nunca deve ser editado manualmente