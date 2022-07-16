from django.forms import ValidationError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

def validate_file(value):
    # title_input = value 
    filename = value.name
    print(dir(value))
    print(not filename.endswith('.pdf'))
    if not filename.endswith('.pdf'):
      message = 'file yang anda upload buka pdf'
      raise ValidationError(_(message))
      # return redirect('administrator:data_trainings')
    # if title_input == 'post 1':
    #   message = 'silakan cari title yang lain!'
    