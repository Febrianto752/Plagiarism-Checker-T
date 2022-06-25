from django.db import models

# Create your models here.
class Admin(models.Model):
  nama = models.CharField(max_length=40)
  username = models.CharField(max_length=40, unique=True)
  password = models.CharField(max_length=100)
  email = models.EmailField(max_length=50)
  no_telp = models.CharField(max_length=14)
  
  def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    super().save(force_insert, force_update, using, update_fields)
    return f'{self.id}. {self.username}'
  
  class Meta:
    db_table = 'administrator'