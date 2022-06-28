from django.forms import ModelForm
from .models import DataTraining

class DataTrainingForm(ModelForm):
  class Meta:
    model = DataTraining
    fields = ['judul', 'penulis', 'tahun', 'file']