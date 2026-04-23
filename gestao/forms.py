from django import forms
from .models import Device, Rack, Sala

class BaseStyledForm(forms.ModelForm):
    base_class = 'form-control rounded-pill px-4'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # Simplificado: aplica a mesma classe base para todos
            field.widget.attrs.update({'class': self.base_class})

class SalaForm(BaseStyledForm):
    class Meta:
        model = Sala
        fields = ['nome', 'localizacao']
        labels = {'nome': 'Nome da Sala', 'localizacao': 'Localização / Bloco'}
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: CPD Principal'}),
            'localizacao': forms.TextInput(attrs={'placeholder': 'Ex: Bloco A, Sala 202'}),
        }

class RackForm(BaseStyledForm):
    class Meta:
        model = Rack
        fields = ['nome', 'sala']
        labels = {'nome': 'Identificação do Rack', 'sala': 'Sala de Destino'}
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Rack-01'}),
        }

class DeviceForm(BaseStyledForm):
    class Meta:
        model = Device
        fields = [
            'serial_id',
            'rack',
            'processador',
            'ram',
            'armazenamento_total_gb',
        ]
        labels = {
            'serial_id': 'ID Serial',
            'rack': 'Rack de Destino',
            'processador': 'Processador',
            'ram': 'Memória RAM',
            'armazenamento_total_gb': 'Armazenamento Total (GB)',
        }
        widgets = {
            'serial_id': forms.TextInput(attrs={'placeholder': 'Ex: DEV-001'}),
            'processador': forms.TextInput(attrs={'placeholder': 'Ex: Intel Core i5'}),
            'ram': forms.TextInput(attrs={'placeholder': 'Ex: 16 GB DDR4'}),
            'armazenamento_total_gb': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Ex: 512'}),
        }

    def __init__(self, *args, **kwargs):
        rack_inicial = kwargs.pop('rack_inicial', None)
        super().__init__(*args, **kwargs)

        if rack_inicial and not self.instance.pk:
            self.fields['rack'].initial = rack_inicial