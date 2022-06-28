from django.db import models
from pdfminer.high_level import extract_text
from .packages.rabin import filterText

# Create your models here.
class SideBySide(models.Model):
  inisial = models.CharField(max_length=20, unique=True)
  text_file1 = models.TextField()
  text_file2 = models.TextField()
  # file1 = models.FileField(upload_to='side_by_side/')
  # file2 = models.FileField(upload_to='side_by_side/')
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  
  class Meta:
    db_table = 'side_by_side'
  
  def __str__(self) -> str:
    return f'{self.id}. {self.inisial}'
  
  def save(self, *args, **kwargs):
    
    # try:
    #   text1 = extract_text(self.file1.file.file)
    #   filter_text1 = filterText(text1)
    #   self.text_file1 = filter_text1
    #   text2 = extract_text(self.file2.file.file)
    #   filter_text2 = filterText(text2)
    #   self.text_file2 = filter_text2
    # except:
    #   self.text_file1 = ''
    #   self.text_file2 = ''
      
    return super().save(*args, **kwargs)
  
  def delete(self, *args, **kwargs):

    
    return super().delete(*args, **kwargs)