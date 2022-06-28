from django.forms import ModelForm 
from .models import SideBySide

class SideBySideForm(ModelForm):
  class Meta:
    model = SideBySide
    # fields = ['']