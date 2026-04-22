from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Device, Rack, Sala
from .forms import SalaForm, RackForm

@login_required
def home(request):
    salas = Sala.objects.all()
    return render(request, 'home.html', {'salas': salas})


@login_required
def sala_detalhe(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    # Busca todos os racks que pertencem a essa sala específica
    racks = sala.racks.all() 
    
    return render(request, 'sala_detalhe.html', {
        'sala': sala,
        'racks': racks
    })


@login_required
def rack_detalhe(request, pk):
    rack = get_object_or_404(Rack, pk=pk)
    # Buscando os dispositivos vinculados ao rack
    devices = rack.devices.all() 
    
    return render(request, 'rack_detalhe.html', {
        'rack': rack,
        'devices': devices
    })


@login_required
def device_detalhe(request, pk):
    device = get_object_or_404(Device, pk=pk)
    return render(request, 'device_detalhe.html', {'device': device})


@login_required
def device_gerenciar(request):
    devices = Device.objects.select_related('rack__sala').all()
    return render(request, 'device_gerenciar.html', {'devices': devices})


@login_required
def device_novo(request):
    return render(request, 'device_form.html')


@login_required
def device_editar(request, pk):
    device = get_object_or_404(Device, pk=pk)
    return render(request, 'device_form.html', {'device': device})


@login_required
def device_excluir(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        device.delete()
        messages.success(request, 'Device excluído com sucesso.')
        return redirect('gestao:device_gerenciar')
    return redirect('gestao:device_gerenciar')

def sala_criar(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestao:home')
    else:
        form = SalaForm()

    return render(request, 'form/generic_form.html', {'form': form, 'titulo': 'Adicionar Sala'})

def rack_criar(request):
    if request.method == 'POST':
        form = RackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestao:home')
    else:
        form = RackForm()

    return render(request, 'form/generic_form.html', {'form': form, 'titulo': 'Adicionar Rack'})