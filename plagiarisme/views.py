from django.urls import resolve
from pdfminer.high_level import extract_text
from django.http import JsonResponse
from django.shortcuts import render
from mahasiswa.models import Mahasiswa, Skripsi
from django.views.generic import View

from administrator.models import DataTraining
from mahasiswa.models import ReportPlagiarism
from .models import SideBySide
from django.contrib import messages
from django.shortcuts import redirect

from .packages.rabin import filterText, createTokens
from .packages.utils import intersection, removeTheSameQuadword, make_quadword_plagiarism_groups, convertStringRepresentationOfListToList


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

  skripsi_mahasiswa = mahasiswa.skripsi.content
  text_data_training = data_training.text_file   

  # fingerprint1
  filter_text1 = filterText(skripsi_mahasiswa)
  tokens_text1 = createTokens(filter_text1)


  # fingerprint2
  filter_text2 = filterText(text_data_training)
  tokens_text2 = createTokens(filter_text2)
  
  unique_tokens_text1 = removeTheSameQuadword(tokens_text1)
  unique_tokens_text2 = removeTheSameQuadword(tokens_text2)

  fingerprint_intersection = intersection(unique_tokens_text1, unique_tokens_text2)
  report_plagiarism = ReportPlagiarism.objects.filter(skripsi_id=mahasiswa.skripsi.id)
  
  
  quadword_plagiarism_groups = None
  if not report_plagiarism.exists():
    quadword_plagiarism_groups = make_quadword_plagiarism_groups([],fingerprint_intersection, data_training)
    report_plagiarism = ReportPlagiarism.objects.create(text_similiarity=str(quadword_plagiarism_groups), skripsi_id = mahasiswa.skripsi.id)

    
  elif report_plagiarism.exists() and not report_plagiarism[0].is_done:
    fingerprints_similiarity = convertStringRepresentationOfListToList(report_plagiarism[0].text_similiarity)
    quadword_plagiarism_groups = make_quadword_plagiarism_groups(fingerprints_similiarity, fingerprint_intersection,  data_training)
    report_plagiarism.update(text_similiarity=str(quadword_plagiarism_groups))
    
  elif report_plagiarism.exists() and report_plagiarism[0].is_done:
    quadword_plagiarism_groups = make_quadword_plagiarism_groups([],fingerprint_intersection,  data_training)
    report_plagiarism.update(text_similiarity=str(quadword_plagiarism_groups), is_done=0)

  if iteration == count:   
    report_plagiarism = ReportPlagiarism.objects.filter(skripsi_id = mahasiswa.skripsi.id)
    report_plagiarism.update(plagiarism_percentage = 101, is_done=1)
    return JsonResponse({'status': 'success', 'is_done': True, 'pk': data_training.id})
     
  else:
    return JsonResponse({'status': 'success', 'is_done': False, 'pk': data_training.id})


def textSimiliarity(request, npm):

  mahasiswa = Mahasiswa.objects.get(npm=npm)
  skripsi_mhs = Skripsi.objects.get(mahasiswa_id = mahasiswa.id)
  report_plagiarism = ReportPlagiarism.objects.get(skripsi_id=skripsi_mhs.id)
  quadword_plagiarism_groups = convertStringRepresentationOfListToList(report_plagiarism.text_similiarity)
 

  return JsonResponse( {'stack_quadword_group': quadword_plagiarism_groups})

def setPlagiarismPercentage(request, *args, **kwargs):
  mahasiswa = Mahasiswa.objects.get(npm=kwargs['npm'])

  mahasiswa.skripsi.reportplagiarism.plagiarism_percentage = kwargs['percentage']
  mahasiswa.skripsi.reportplagiarism.save()
  
  return JsonResponse({'status': 'success'})

# Halaman detail plagiarism 
class SimiliarityBetweenTwoThesis(View):
  template_name = 'mahasiswa/detail_report.html'
  
  def get(self, *args, **kwargs):
 
    npm_mhs = kwargs['npm_mhs']
    id_data_training = kwargs['id_data_training']
    
    mahasiswa = Mahasiswa.objects.get(npm = npm_mhs)

    content_skripsi_mhs = mahasiswa.skripsi.content
    
    data_training = DataTraining.objects.get(id = id_data_training)

    text_data_training = data_training.text_file
    
    

    context = {
      'title': 'plagiarism between of two thesis',
      'text_skripsi_mhs': content_skripsi_mhs,
      'text_data_training': text_data_training,
      'mahasiswa': mahasiswa,
      'data_training': data_training
    }
    
    return render(self.request, self.template_name, context)

def similiarityOneToOne(request, *args, **kwargs):
  npm_mhs = kwargs['npm_mhs']
  id_data_training = kwargs['id_data_training']
  
  mahasiswa = Mahasiswa.objects.get(npm = npm_mhs)
  content_skripsi_mhs = mahasiswa.skripsi.content
  
  data_training = DataTraining.objects.get(id = id_data_training)
  text_data_training = data_training.text_file
  
  # fingerprint1
  tokens_text1 = createTokens(content_skripsi_mhs)



  # fingerprint2
  tokens_text2 = createTokens(text_data_training)

  unique_tokens_text1 = removeTheSameQuadword(tokens_text1)
  unique_tokens_text2 = removeTheSameQuadword(tokens_text2)

  fingerprint_intersection = intersection(unique_tokens_text1, unique_tokens_text2)
  quadword_plagiarism_groups = make_quadword_plagiarism_groups([],fingerprint_intersection, data_training)
  
  del quadword_plagiarism_groups[0][0]
  return JsonResponse({'stack_quadword_group': quadword_plagiarism_groups[0]})


class SideBySideView(View):
  template_name = 'plagiarisme/side_by_side.html'
  context = {
    'title': 'test compare side by side'
  }

  def get(self, *args, **kwargs):
    # self.context['coba'] = [[123],2,3]
    current_url = resolve(self.request.path_info).url_name
    self.context['current_url'] = current_url
    return render(self.request, self.template_name, self.context)
  
  def post(self, *args, **kwargs):
    if not self.request.FILES['file1'].name.endswith('.pdf') or not self.request.FILES['file2'].name.endswith('.pdf'):
        messages.error(self.request, 'file yang anda upload harus pdf...') # mengirimkan flash message error
        return redirect('plagiarisme:side_by_side_test')
    # fingerprint1
    text_file1 = extract_text(self.request.FILES['file1'].file)
    filter_text1 = filterText(text_file1)
    


    # fingerprint2
    text_file2 = extract_text(self.request.FILES['file2'].file)
    filter_text2 = filterText(text_file2)
    
    exist_row = SideBySide.objects.filter(inisial=self.request.session['username'])
    if exist_row.exists():
      exist_row.update(text_file1 = filter_text1, text_file2=filter_text2)
    else: 
      SideBySide.objects.create(inisial=self.request.session['username'], text_file1 = filter_text1, text_file2=filter_text2)
      
    self.context['text_file1'] = filter_text1
    self.context['text_file2'] = filter_text2
    self.context['finish_upload'] = 'true'
     
    return render(self.request, self.template_name, self.context)
    
def sideBySidePlagiarismCheck(request, inisial):
  sideBySideRow = SideBySide.objects.filter(inisial=inisial)
  
  if sideBySideRow.exists():
    text1 = sideBySideRow[0].text_file1   
    text2 = sideBySideRow[0].text_file2   
      
    tokens_text1 = createTokens(text1)
      
    tokens_text2 = createTokens(text2)
    
    unique_tokens_text1 = removeTheSameQuadword(tokens_text1)
    unique_tokens_text2 = removeTheSameQuadword(tokens_text2)

    intersection_text1_2 = intersection(unique_tokens_text1, unique_tokens_text2)

    quadword_groups = make_quadword_plagiarism_groups([], intersection_text1_2, '')

    del quadword_groups[0][0]
  
    return JsonResponse({'stack_quadword_group': quadword_groups, 'text1': text1, 'text2': text2})
  
  else:
    return JsonResponse({'status': 'failed'})



