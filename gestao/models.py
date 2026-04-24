from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

STATUS_CHOICES = [
    ('conectado_carregando', 'Conectado e carregando'),
    ('conectado', 'Conectado'),
    ('desconectado', 'Desconectado'),
    ('problema', 'Problema'),
]


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
        return f'{self.nome} - {self.sala.nome}'


class Device(models.Model):
    serial_id = models.CharField(max_length=20, unique=True)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name='devices')
    processador = models.CharField(max_length=100)
    ram = models.CharField(max_length=20)
    armazenamento_total_gb = models.PositiveIntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['serial_id']
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return f'{self.serial_id} - {self.rack.nome}'

    @property
    def tem_telemetria(self):
        return hasattr(self, 'telemetria_atual')


class DeviceTelemetry(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='telemetria_atual')
    bateria_pct = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    status_conexao = models.CharField(max_length=25, choices=STATUS_CHOICES, default='desconectado')
    armazenamento_usado_gb = models.PositiveIntegerField(default=0)
    ultimo_log = models.DateTimeField()
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Telemetria atual'
        verbose_name_plural = 'Telemetrias atuais'

    def clean(self):
        """Valida se o armazenamento usado não excede o total do hardware."""
        if self.device and self.armazenamento_usado_gb > self.device.armazenamento_total_gb:
            raise ValidationError({
                'armazenamento_usado_gb': f"Uso ({self.armazenamento_usado_gb}GB) excede o total ({self.device.armazenamento_total_gb}GB)."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Telemetria de {self.device.serial_id}'


class TelemetryLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='logs')
    bateria_pct = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    status_conexao = models.CharField(max_length=25, choices=STATUS_CHOICES)
    armazenamento_usado_gb = models.PositiveIntegerField()
    registrado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registrado_em']
        verbose_name = 'Log de telemetria'
        verbose_name_plural = 'Logs de telemetria'

    def clean(self):
        """Impede o registro de logs com armazenamento inconsistente."""
        if self.device and self.armazenamento_usado_gb > self.device.armazenamento_total_gb:
            raise ValidationError({
                'armazenamento_usado_gb': "O armazenamento usado no log não pode ser maior que o total do dispositivo."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.device.serial_id} - {self.registrado_em}'
