import os
from django.db import models
from django.dispatch import receiver
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
    # print(dir(self.path_file.file.file))
    # raise SystemExit
    try:
      text = str(extract_text(self.path_file.file.file))
      filter_text = str(filterText(text))
      # print(filter_text)
      self.text_file = str(filter_text)
    except:
      self.text_file = ''
    
    return super().save()
  
  def delete(self, *args, **kwargs):
    # print(dir(self.path_file))
    # print(self.path_file.path)
    os.remove(self.path_file.path)
    
    return super().delete(*args,**kwargs)
  
  
  def __str__(self) -> str:
    return f'{self.id}. {self.author}'
  
  
  
  class Meta: 
    db_table = 'data_training'
    
# # jika user update data table skripsi maka file old pdf akan dihapus
# @receiver(models.signals.pre_save, sender=DataTraining)
# def auto_delete_file_skripsi_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `DataTraining` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False

#     try:
#         old_file = DataTraining.objects.get(pk=instance.pk).pdf
#     except DataTraining.DoesNotExist:
#         return False

#     new_file = instance.pdf
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)