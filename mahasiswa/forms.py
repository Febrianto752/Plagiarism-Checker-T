from django.forms import ModelForm
from .models import Mahasiswa, Skripsi

class SkripsiForm(ModelForm):
  class Meta:
    model = Skripsi 
    fields = ['pdf']
    
  def __init__(self, *args, **kwargs):
    if args:
      self.npm = args[0]['npm']
    
    return super().__init__(*args, **kwargs)
  
  
  def save(self, commit=True):
    instance = super().save(commit=False)
    instance.mahasiswa = Mahasiswa.objects.get(npm=self.npm)
    
    if commit:
      instance.save()
    
    return instance