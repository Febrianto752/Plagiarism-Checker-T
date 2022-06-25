from django.core.management.base import BaseCommand
from django_seed import Seed
# from mahasiswa.models import Mahasiswa, DosenPembimbing
from administrator.models import Admin

class Command(BaseCommand):
  help = 'adminSeed'

  def handle(self, *args, **kwargs):
    print('hello')
    

    seeder = Seed.seeder()
    seeder.add_entity(Admin, 1, {
        'username': 'febrianto',
        'nama': 'febrianto',
        'password': 'febri123'
    })

    # seeder.add_entity(Admin, 5)
    # seeder.add_entity(Mahasiswa, 20)
    # seeder.add_entity(Player, 10)

    inserted_pks = seeder.execute()