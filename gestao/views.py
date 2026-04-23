from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DeviceForm, RackForm, SalaForm
from .models import Device, Rack, Sala, TelemetryLog


@login_required
def home(request):
    query = request.GET.get('search')
    if query:
        # Busca no nome ou na localização
        salas = Sala.objects.filter(
            Q(nome__icontains=query) | Q(localizacao__icontains=query)
        ).distinct()
    else:
        salas = Sala.objects.all()
    return render(request, 'home.html', {'salas': salas})


@login_required
def sala_detalhe(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    query = request.GET.get('search')
    racks = Rack.objects.filter(sala=sala)

    if query:
        racks = racks.filter(Q(nome__icontains=query)).distinct()

    return render(request, 'sala_detalhe.html', {'sala': sala, 'racks': racks})


@login_required
def rack_detalhe(request, pk):
    rack = get_object_or_404(Rack.objects.select_related('sala'), pk=pk)
    query = request.GET.get('search')
    devices = Device.objects.filter(rack=rack).select_related('telemetria_atual')

    if query:
        devices = devices.filter(
            Q(serial_id__icontains=query) | Q(processador__icontains=query)
        ).distinct()

    return render(request, 'rack_detalhe.html', {'rack': rack, 'devices': devices})


@login_required
def device_detalhe(request, pk):
    device = get_object_or_404(
        Device.objects.select_related('rack__sala', 'telemetria_atual').prefetch_related(
            Prefetch('logs', queryset=TelemetryLog.objects.order_by('-registrado_em'))
        ),
        pk=pk,
    )
    telemetria = getattr(device, 'telemetria_atual', None)
    logs = list(device.logs.all()[:10])
    uso_pct = None

    if telemetria and device.armazenamento_total_gb:
        uso_pct = min(
            100,
            round((telemetria.armazenamento_usado_gb / device.armazenamento_total_gb) * 100),
        )

    context = {
        'device': device,
        'telemetria': telemetria,
        'logs': logs,
        'uso_pct': uso_pct,
    }
    return render(request, 'device_detalhe.html', context)


@login_required
def device_gerenciar(request):
    return redirect('gestao:home')


@login_required
def device_novo(request):
    rack_id = request.GET.get('rack')
    rack = get_object_or_404(Rack, pk=rack_id) if rack_id else None

    if request.method == 'POST':
        form = DeviceForm(request.POST, rack_inicial=rack)
        if form.is_valid():
            device = form.save()
            return redirect('gestao:rack_detalhe', pk=device.rack.pk)
    else:
        form = DeviceForm(rack_inicial=rack)

    return render(request, 'form/generic_form.html', {'form': form, 'titulo': 'Adicionar Device'})


@login_required
def device_editar(request, pk):
    device = get_object_or_404(Device, pk=pk)

    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            device = form.save()
            return redirect('gestao:rack_detalhe', pk=device.rack.pk)
    else:
        form = DeviceForm(instance=device)

    return render(request, 'form/generic_form.html', {'form': form, 'titulo': f'Editar {device.serial_id}'})


@login_required
def device_excluir(request, pk):
    device = get_object_or_404(Device, pk=pk)
    rack_id = device.rack.id

    if request.method == 'POST':
        device.delete()
        messages.success(request, 'Device excluído com sucesso.')
        return redirect('gestao:rack_detalhe', pk=rack_id)

    return render(request, 'form/confirmar_exclusao.html', {
        'objeto': device,
        'tipo': 'Device',
        'titulo': f'Excluir {device.serial_id}',
    })

@login_required
def sala_criar(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestao:home')
    else:
        form = SalaForm()

    return render(request, 'form/generic_form.html', {'form': form, 'titulo': 'Adicionar Sala'})

@login_required
def rack_criar(request):
    if request.method == 'POST':
        form = RackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestao:home')
    else:
        form = RackForm()

    return render(request, 'form/generic_form.html', {'form': form, 'titulo': 'Adicionar Rack'})

@login_required
def sala_editar(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            return redirect('gestao:home')
    else:
        form = SalaForm(instance=sala)
    return render(request, 'form/generic_form.html', {'form': form, 'titulo': f'Editar {sala.nome}'})

@login_required
def rack_editar(request, pk):
    rack = get_object_or_404(Rack, pk=pk)
    sala_id = rack.sala.id

    if request.method == 'POST':
        form = RackForm(request.POST, instance=rack)
        if form.is_valid():
            form.save()
            return redirect('gestao:sala_detalhe', pk=sala_id)
    else:
        form = RackForm(instance=rack)
    return render(request, 'form/generic_form.html', {'form': form, 'titulo': f'Editar {rack.nome}'})

@login_required
def sala_deletar(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        sala.delete()
        return redirect('gestao:home')
    return render(request, 'form/confirmar_exclusao.html', {'objeto': sala, 'tipo': 'Sala', 'titulo': f'Excluir {sala.nome}'})

@login_required
def rack_deletar(request, pk):
    rack = get_object_or_404(Rack, pk=pk)
    sala_id = rack.sala.id

    if request.method == 'POST':
        rack.delete()
        return redirect('gestao:sala_detalhe', pk=sala_id)
    return render(request, 'form/confirmar_exclusao.html', {'objeto': rack, 'tipo': 'Rack', 'titulo': f'Excluir {rack.nome}'})
