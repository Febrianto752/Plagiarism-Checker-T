import ast
def intersection(list1, list2):
    intersection_list = [value for value in list1 if value in list2]
    return intersection_list

def convertStringRepresentationOfListToList(string):
  result = ast.literal_eval(string)
  
  return result



# remove the same hash and get just value hash (not with index)
def removeTheSameQuadword(quadwords):
    filter_quadwords = []

    for quadword in quadwords:
        if not (quadword in filter_quadwords):
            filter_quadwords.append(quadword)
    
    return filter_quadwords






# ------------- NEW ------------------
def make_quadword_plagiarism_groups(quadword_groups:list, new_quadwords:list, object):
  # contoh hash group : [['satu', 1,2,5], ['dua', 3,4,6], ['tiga', 9,8,7]]
  # contoh new_quadwords = [hash1, hash2]
  
  
  if object != '':
    source = [object.id, f'{object.penulis}. "{object.judul}". {object.tahun}']
  else:
    source = ''
  # jika quadword_groups masih kosong 
  if len(quadword_groups) == 0:
    first_group = [source, *new_quadwords]
    quadword_groups.append(first_group)
    # output : [[values]]
  
  else:
    new_group = []
    tmp_all_group = []
    for group in quadword_groups:
      tmp_all_group = [*tmp_all_group, *group]
      
    # for group in quadword_groups:
      
    new_group = [*[new_quadword for new_quadword in new_quadwords if new_quadword not in tmp_all_group]]

    new_group.insert(0, source)      
    quadword_groups.append(new_group)    
      
      
  return quadword_groups




# --- ONE TO ONE
