from django.db import models
from pdfminer.high_level import extract_text
from plagiarisme.packages.rabin import filterText
# Create your models here.
class Admin(models.Model):
  nama = models.CharField(max_length=40)
  username = models.CharField(max_length=40, unique=True)
  password = models.CharField(max_length=100)
  email = models.EmailField(max_length=50)
  no_telp = models.CharField(max_length=14)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  
  def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    super().save(force_insert, force_update, using, update_fields)
    return f'{self.id}. {self.username}'
  
  class Meta:
    db_table = 'administrator'
    
class DataTraining(models.Model):
  author = models.CharField(max_length=30)
  tahun = models.IntegerField(null=True)
  text_file = models.TextField()
  path_file = models.FileField(upload_to='data_trainings/')
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  
  def save(self, *args, **kwargs):
    print(dir(self.path_file.file.file))
    # raise SystemExit
    text = extract_text(self.path_file.file.file)
    filter_text = filterText(text)
    self.text_file = filter_text
    
    return super().save()
  
  def __str__(self) -> str:
    return f'{self.id}. {self.author}'
  
  class Meta: 
    db_table = 'data_training'