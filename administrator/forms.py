from django.forms import FileInput, ModelForm, NumberInput, TextInput
from .models import DataTraining

class DataTrainingForm(ModelForm):

  
  class Meta:
    model = DataTraining
    fields = ['judul', 'penulis', 'tahun', 'file']
    
    widgets = {
      'judul': TextInput(attrs={
        'class': 'form-control'
      }),
      'penulis': TextInput(attrs={
        'class': 'form-control'
      }),
      'tahun': NumberInput(attrs={
        'class': 'form-control'
      }),
      'file': FileInput(attrs={
        'class': 'form-control',
        'accept': '.pdf'
      })
    }