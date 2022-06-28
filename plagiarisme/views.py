from time import time
from django.http import JsonResponse
from django.shortcuts import render
from mahasiswa.models import Mahasiswa, Skripsi
from django.views.generic import DetailView, View

from administrator.models import DataTraining
from mahasiswa.models import ReportPlagiarism
from plagiarisme.packages.rabin import createHashesMD5, createTokens, filterText
from plagiarisme.packages.utils import convertStringRepresentationOfListToList, get_hash_plagiarism_groups_with_index, get_quadword_from_hash, intersection, make_hash_plagiarism_groups, make_stack_quadword_group, removeTheSameHash
# Create your views here.

# === Tampilan Halaman ===
class CekPlagiarisme(View):
  template_name = 'plagiarisme/cek_plagiarisme.html'
  context = {
    'title': 'cek plagiarisme'
  }
  
  def get(self, *args, **kwargs):
    object = Mahasiswa.objects.get(npm=kwargs['npm'])
    self.context['object'] = object
    return render(self.request, self.template_name, self.context)
    
  
  
  
  
  
  
  
  
  
  
# == Process ==
def checking(request, npm, iteration, pk, count):
  # npm untuk mengambil skripsi si mahasiswanya
  # pk for skripsi yang mau dibandingkan terurut
  # count = jumlah data training / jumlah skripsi

  mahasiswa = Mahasiswa.objects.get(npm=npm)
  # jika mahasiswa belum upload file skripsi 
  try:
    tmp = mahasiswa.skripsi
  except AttributeError:
    # jika mahasiswa belum upload skripsi 
    return JsonResponse({'error': 1})



  if not DataTraining.objects.all().exists():
    return JsonResponse({'error': 2})
  
  if iteration == 1:
    data_training = DataTraining.objects.all()[0]
    
        
  else:
    data_training = DataTraining.objects.raw(f"SELECT id, penulis, text_file FROM data_training WHERE id > {pk} LIMIT 1")[0]
  print(pk)
  print(data_training)
  # if '?' in mahasiswa.skripsi.content: 
  #     # print('?????')
  #     # mahasiswa.skripsi.content = mahasiswa.skripsi.content.replace('?','')
  #     # print(mahasiswa.skripsi.content)
  #     mahasiswa.skripsi.save()
  skripsi_mahasiswa = mahasiswa.skripsi.content
  text_data_training = data_training.text_file   
  
  # report_plagiarism = ReportPlagiarism.objects.get(skripsi_id=38)
  # print(dir(report_plagiarism))

  # fingerprint1
  filter_text1 = filterText(skripsi_mahasiswa)
  # print(filter_text1)
  tokens_text1 = createTokens(filter_text1)
  hashesMD5_text1 = createHashesMD5(tokens_text1)


  # fingerprint2
  filter_text2 = filterText(text_data_training)
  tokens_text2 = createTokens(filter_text2)
  hashesMD5_text2 = createHashesMD5(tokens_text2)

  unique_hashesMD51 = removeTheSameHash(hashesMD5_text1)
  unique_hashesMD52 = removeTheSameHash(hashesMD5_text2)


  fingerprint_intersection = intersection(unique_hashesMD51, unique_hashesMD52)
  report_plagiarism = ReportPlagiarism.objects.filter(skripsi_id=mahasiswa.skripsi.id)
  
  
  hash_plagiarism_groups = None
  if not report_plagiarism.exists():
    hash_plagiarism_groups = make_hash_plagiarism_groups([],fingerprint_intersection, data_training)
    report_plagiarism = ReportPlagiarism.objects.create(text_similiarity=str(hash_plagiarism_groups), skripsi_id = mahasiswa.skripsi.id)

    
  elif report_plagiarism.exists() and not report_plagiarism[0].is_done:
    fingerprints_similiarity = convertStringRepresentationOfListToList(report_plagiarism[0].text_similiarity)
    hash_plagiarism_groups = make_hash_plagiarism_groups(fingerprints_similiarity, fingerprint_intersection,  data_training)
    report_plagiarism.update(text_similiarity=str(hash_plagiarism_groups))
    print('dua')
    
  elif report_plagiarism.exists() and report_plagiarism[0].is_done:
    hash_plagiarism_groups = make_hash_plagiarism_groups([],fingerprint_intersection,  data_training)
    report_plagiarism.update(text_similiarity=str(hash_plagiarism_groups), is_done=0)
    print('tiga')
  
  # count = jumlah skripsi 
  # jika iteration = jumlah skripsi - skripsi yang dicek(1)
  
  # count = jumlah skripsi 
  # jika iteration = jumlah skripsi - skripsi yang dicek(1)
  if iteration == count:   
    print('hello')   

    # jika ada lebih dari satu skripsi yg dibandingkan
    # path_dir_report = f'mahasiswa/reports/{npm}_{time.time()}.pdf'
    # if hash_plagiarism_groups:
    #   # percent = checkSimiliarity2(unique_hashesMD51, hash_plagiarism_groups)
    #   percent = 10.23
    #   print(percent)

    # else:
    #   # percent = checkSimiliarity2(unique_hashesMD51, unique_hashesMD52)
    #   percent = 22
    #   print(percent)

    report_plagiarism = ReportPlagiarism.objects.filter(skripsi_id = mahasiswa.skripsi.id)
    report_plagiarism.update(plagiarism_percentage = 101, is_done=1)
    return JsonResponse({'status': 'success', 'is_done': True, 'pk': data_training.id})
     
  else:
    return JsonResponse({'status': 'success', 'is_done': False, 'pk': data_training.id})




def textSimiliarity(request, npm):
  print(npm)
  mahasiswa = Mahasiswa.objects.get(npm=npm)
  skripsi_mhs = Skripsi.objects.get(mahasiswa_id = mahasiswa.id)
  report_plagiarism = ReportPlagiarism.objects.get(skripsi_id=skripsi_mhs.id)
  hash_plagiarism_groups = convertStringRepresentationOfListToList(report_plagiarism.text_similiarity)
  
  # skripsi mhs 
  tokens_skipsi_mhs = createTokens(skripsi_mhs.content)
  hashes_with_index_skripsi_mhs = createHashesMD5(tokens_skipsi_mhs)
  
  # plagiarism detection 
  hash_plagiarism_groups_with_index = get_hash_plagiarism_groups_with_index(hash_plagiarism_groups, hashes_with_index_skripsi_mhs)
  quadword_groups = get_quadword_from_hash(hash_plagiarism_groups_with_index, tokens_skipsi_mhs)

  stack_quadword_group = make_stack_quadword_group(quadword_groups)
  print(len(stack_quadword_group))
  return JsonResponse( {'stack_quadword_group': stack_quadword_group})
  # return JsonResponse({'text_of_plagiarism': stack_quadword_group, 'stack_quadword_group': stack_quadword_group})



def setPlagiarismPercentage(request, *args, **kwargs):
  mahasiswa = Mahasiswa.objects.get(npm=kwargs['npm'])
  print(mahasiswa.skripsi.reportplagiarism.plagiarism_percentage)
  print(kwargs['percentage'])
  mahasiswa.skripsi.reportplagiarism.plagiarism_percentage = kwargs['percentage']
  mahasiswa.skripsi.reportplagiarism.save()
  
  return JsonResponse({'status': 'success'})