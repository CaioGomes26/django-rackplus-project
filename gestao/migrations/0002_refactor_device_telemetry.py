from django.db import migrations, models
import django.db.models.deletion


def migrar_telemetria_para_modelo_atual(apps, schema_editor):
    Device = apps.get_model('gestao', 'Device')
    DeviceTelemetry = apps.get_model('gestao', 'DeviceTelemetry')

    for device in Device.objects.all():
        tem_dados_reais = (
            device.ultimo_log is not None
            or device.bateria_pct != 0
            or device.armazenamento_usado_gb != 0
            or device.status_conexao != 'desconectado'
        )

        if tem_dados_reais:
            DeviceTelemetry.objects.update_or_create(
                device_id=device.id,
                defaults={
                    'bateria_pct': device.bateria_pct,
                    'status_conexao': device.status_conexao,
                    'armazenamento_usado_gb': device.armazenamento_usado_gb,
                    'ultimo_log': device.ultimo_log,
                },
            )


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceTelemetry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bateria_pct', models.PositiveIntegerField(default=0)),
                ('status_conexao', models.CharField(choices=[('conectado_carregando', 'Conectado e carregando'), ('conectado', 'Conectado'), ('desconectado', 'Desconectado'), ('problema', 'Problema')], default='desconectado', max_length=25)),
                ('armazenamento_usado_gb', models.PositiveIntegerField(default=0)),
                ('ultimo_log', models.DateTimeField()),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='telemetria_atual', to='gestao.device')),
            ],
            options={
                'verbose_name': 'Telemetria atual',
                'verbose_name_plural': 'Telemetrias atuais',
            },
        ),
        migrations.RunPython(migrar_telemetria_para_modelo_atual, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='device',
            name='armazenamento_usado_gb',
        ),
        migrations.RemoveField(
            model_name='device',
            name='bateria_pct',
        ),
        migrations.RemoveField(
            model_name='device',
            name='status_conexao',
        ),
        migrations.RemoveField(
            model_name='device',
            name='ultimo_log',
        ),
        migrations.AlterField(
            model_name='telemetrylog',
            name='status_conexao',
            field=models.CharField(choices=[('conectado_carregando', 'Conectado e carregando'), ('conectado', 'Conectado'), ('desconectado', 'Desconectado'), ('problema', 'Problema')], max_length=25),
        ),
    ]
