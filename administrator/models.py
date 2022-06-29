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
  judul = models.CharField(max_length=70, null=True)
  penulis = models.CharField(max_length=50, null=True)
  tahun = models.IntegerField(null=True)
  text_file = models.TextField()
  file = models.FileField(upload_to='data_trainings/')
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  
  class Meta: 
    db_table = 'data_training'
    
  def __str__(self) -> str:
    return f'{self.id}. {self.judul}'
  
  def save(self):
    
    try:
      text = extract_text(self.file.file.file)
      filter_text = filterText(text)
      # print(filter_text)
      self.text_file = filter_text
    except:
      self.text_file = ''
    
    return super().save()
  
  def delete(self, *args, **kwargs):
    self.file.delete()
    
    return super().delete(*args, **kwargs)

  # def get_absolute_url(self):
  #   url_slug = {
  #     'pk':self.id
  #   }
  #   return reverse('administrator:detail_mahasiswa')

# jika user update data table skripsi maka file old pdf akan dihapus
# @receiver(models.signals.pre_save, sender=DataTraining)
# def auto_delete_file_datatraining_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `Skripsi` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False

#     try:
#         old_file = DataTraining.objects.get(pk=instance.pk).file
#     except DataTraining.DoesNotExist:
#         return False

#     new_file = instance.file
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
  