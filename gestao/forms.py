from django import forms
from .models import Sala, Rack

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