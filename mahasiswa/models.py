import os
from django.db import models
from django.dispatch import receiver
from pdfminer.high_level import extract_text
from plagiarisme.packages.rabin import filterText


class Mahasiswa(models.Model):
  npm = models.CharField(max_length=20, unique=True)
  nama = models.CharField(max_length=100)
  password = models.CharField(max_length=100)
  jurusan = models.CharField(max_length=20)
  email = models.EmailField(max_length=100, null=True, blank=True)
  no_telp = models.CharField(max_length=20, null=True, blank=True)
  semester = models.IntegerField()
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  
  def __str__(self) -> str:
    return f'{self.id}. {self.nama}'
  
  class Meta: 
    db_table = 'mahasiswa'

class Skripsi(models.Model):
  content = models.TextField()
  pdf = models.FileField(upload_to='mahasiswa/skripsi/')
  mahasiswa = models.OneToOneField(Mahasiswa, on_delete=models.CASCADE)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  
  def save(self, *args,**kwargs):
    
    try:
      text = extract_text(self.pdf.file.file)
      filter_text = filterText(text)
      # print(filter_text)
      self.content = filter_text
    except:
      self.content = ''
    
    if ReportPlagiarism.objects.filter(skripsi_id = self.id).exists():
      ReportPlagiarism.objects.get(skripsi_id=self.id).delete()
    
    return super().save(*args,**kwargs)
  
  def __str__(self) -> str:
     return f'{self.id}. {self.mahasiswa}'
  
  def delete(self, *args, **kwargs):
    self.pdf.delete()
    
    return super().delete(*args, **kwargs)

  class Meta: 
    db_table = 'skripsi'
  

# jika user update data table skripsi maka file old pdf akan dihapus
@receiver(models.signals.pre_save, sender=Skripsi)
def auto_delete_file_skripsi_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Skripsi` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Skripsi.objects.get(pk=instance.pk).pdf
    except Skripsi.DoesNotExist:
        return False

    new_file = instance.pdf
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class ReportPlagiarism(models.Model):
  text_similiarity = models.TextField(null=True)
  plagiarism_percentage = models.FloatField(null=True)
  is_done = models.BooleanField(default=False)
  skripsi = models.OneToOneField(Skripsi, on_delete=models.CASCADE)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  
  def __str__(self) -> str:
    return f'{self.id}. {self.is_done}'
  
  class Meta: 
    db_table = 'report_plagiarism'
