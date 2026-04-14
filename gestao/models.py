from django.db import models


class Sala(models.Model):
    nome = models.CharField(max_length=50)
    localizacao = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return self.nome


class Rack(models.Model):
    nome = models.CharField(max_length=50)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='racks')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Rack'
        verbose_name_plural = 'Racks'

    def __str__(self):
        return f'{self.nome} — {self.sala.nome}'


class Device(models.Model):

    STATUS_CHOICES = [
        ('conectado_carregando', 'Conectado e carregando'),
        ('conectado',            'Conectado'),
        ('desconectado',         'Desconectado'),
        ('problema',             'Problema'),
    ]

    serial_id = models.CharField(max_length=20, unique=True)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name='devices')

    # Especificações técnicas do aparelho
    processador = models.CharField(max_length=100)
    ram = models.CharField(max_length=20)
    armazenamento_total_gb = models.PositiveIntegerField()
    armazenamento_usado_gb = models.PositiveIntegerField(default=0)

    # Telemetria atual — atualizada pelo script externo via API
    bateria_pct = models.PositiveIntegerField(default=0)
    status_conexao = models.CharField(max_length=25, choices=STATUS_CHOICES, default='desconectado')
    ultimo_log = models.DateTimeField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['serial_id']
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return f'{self.serial_id} — {self.rack.nome}'


class TelemetryLog(models.Model):
    # Cada registro é um snapshot do estado do device em um momento
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='logs')

    # Cópia dos valores no momento do registro
    bateria_pct = models.PositiveIntegerField()
    status_conexao = models.CharField(max_length=25)
    armazenamento_usado_gb = models.PositiveIntegerField()

    registrado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registrado_em']  # mais recente primeiro
        verbose_name = 'Log de telemetria'
        verbose_name_plural = 'Logs de telemetria'

    def __str__(self):
        return f'{self.device.serial_id} — {self.registrado_em}'