import ast
def intersection(list1, list2):
    intersection_list = [value for value in list1 if value in list2]
    return intersection_list

# def notIntersection(list1, list2):
#   not_intersection_list = [value for value in list1 if value not in list2]
#   return not_intersection_list

# def enterTheNewHashes(hashes, new_hashes):
#   for new_hash in new_hashes:
#     if new_hash not in hashes:
#       hashes.append(new_hash)
  
#   return hashes

# def checkSimiliarity(fingerprint1, fingerprint2):
#   set_fingerprint1 = set(fingerprint1)
#   set_fingerprint2 = set(fingerprint2)
  
#   percent_similiarity = (len(set_fingerprint1.intersection(set_fingerprint2)) / len(set_fingerprint1.union(set_fingerprint2))) * 100
  
#   return percent_similiarity
  
def convertStringRepresentationOfListToList(string):
  result = ast.literal_eval(string)
  
  return result


def matchHash2(intersection_fingerprint, hashes_md5_text):
  # intersection_fingerprint = kumpulan hash saja
  # hashes_md5_text = kumpulan [hash, index]
  hashes = [value for value in hashes_md5_text if value[0] in intersection_fingerprint]
  

  return hashes


def matchIndexHashWithWord(hashes, tokens):
  # hashes = kumpulan [hash, index]
  # tokens = kumpulan [nword, index]
  nword = []
  for token in tokens:
    for hash in hashes:
      if token[1] == hash[1] and token[0] not in nword:
        nword.append(token[0])

  return nword


# def checkSimiliarity2(fingerprint1, fingerprint2):
#   set_fingerprint1 = set(fingerprint1)
#   set_fingerprint2 = set(fingerprint2)
  
#   percent_similiarity = (len(set_fingerprint1.intersection(set_fingerprint2)) / len(set_fingerprint1)) * 100
  
#   return percent_similiarity

# remove the same hash and get just value hash (not with index)
def removeTheSameHash(hashes):
    filter_hashes = []

    for hash in hashes:
        if not (hash[0] in filter_hashes):
            filter_hashes.append(hash[0])
    
    return filter_hashes



def stack_nword(nword):
  i = 0
  stacks = []
  stack = ''
  while i < len(nword):
    if i < 1 or stack == '':
      stack += nword[i][0] + ' '
    elif i >= 1:
      if len(stack.split(' ')) > 9:
        stacks.append(stack.rstrip())
        stack = ''
      elif nword[i][0].split(' ')[1] == nword[i-1][0].split(' ')[2]:
        stack += nword[i][0].split(' ')[2] + ' '
        
        if i == len(nword) - 1:
          stacks.append(stack.rstrip())
          stack = ''

      else:
        stacks.append(stack.rstrip())
        stack = ''

    i += 1
    
  return stacks


def stack_triword(nword:list):
  # nword = kumpulan [nword] 
  i = 0
  stacks = []
  stack = ''
  while i < len(nword):
    if i < 1 or stack == '':
      stack += nword[i] + ' '
    elif i >= 1:
      if len(stack.split(' ')) > 9:
        stacks.append(stack.rstrip())
        stack = ''
      elif nword[i].split(' ')[1] == nword[i-1].split(' ')[2]:
        stack += nword[i].split(' ')[2] + ' '
        
        if i == len(nword) - 1:
          stacks.append(stack.rstrip())
          stack = ''

      else:
        stacks.append(stack.rstrip())
        stack = ''
    
    # print(stacks)
    i += 1
    
  return stacks

def stack_quad_word(nword):
  i = 0
  stacks = []
  stack = ''
  while i < len(nword):
    if i < 1 or stack == '':
      stack += nword[i] + ' '
    elif i >= 1:
      if len(stack.split(' ')) > 12:
        stacks.append(stack.rstrip())
        stack = ''
      elif nword[i].split(' ')[2] == nword[i-1].split(' ')[3]:
        stack += nword[i].split(' ')[3] + ' '
        
        if i == len(nword) - 1:
          stacks.append(stack.rstrip())
          stack = ''

      else:
        stacks.append(stack.rstrip())
        stack = ''
    
    i += 1
    
  return stacks







# ------------- NEW ------------------
def make_hash_plagiarism_groups(hash_groups:list, new_hashes:list, object):
  # contoh hash group : [['satu', 1,2,5], ['dua', 3,4,6], ['tiga', 9,8,7]]
  # contoh new_hashes = [hash1, hash2]
  
  # jika hash_groups masih kosong 
  source = [object.id,f'{object.penulis}. "{object.judul}". {object.tahun}']
  if len(hash_groups) == 0:
    first_group = [source, *new_hashes]
    hash_groups.append(first_group)
    # output : [[values]]
  
  else:
    new_group = []
    tmp_all_group = []
    for group in hash_groups:
      tmp_all_group = [*tmp_all_group, *group]
      
    for group in hash_groups:
      
      new_group = [*new_group, *[new_hash for new_hash in new_hashes if new_hash not in tmp_all_group and new_hash not in new_group]]

    new_group.insert(0, source)      
    hash_groups.append(new_group)    
      
      
  return hash_groups


def get_hash_plagiarism_groups_with_index(hash_groups:list, hashes_with_index:list):
  # hash_groups = [['lead1', hashn...], ['lead2',hashx...], ...]
  # hash_with_index = [[hash, index]...]
  hash_groups_with_index = []
  hash_group_with_index = []
  
  for hash_group in hash_groups:
    hash_group_with_index = [value for value in hashes_with_index if value[0] in hash_group]
    hash_group_with_index.insert(0, hash_group[0])
    hash_groups_with_index.append(hash_group_with_index)
    hash_group_with_index = []
  
  # return [['lead1', (hash, index)], ['lead2',(hash, index)], ...]
  return hash_groups_with_index 

def get_quadword_from_hash(hash_groups:list, tokens_quadword_with_index: list):
  # hash_groups = [['lead1', (hash1, index1)], ['lead2' , (hash2, index2)]]
  # tokens_quadword_with_index = [(quadword1, index1), (quadword2, index2)]
  quad_word_groups = []
  quad_word_group = []
  
  for hash_group in hash_groups:
    first_value = hash_group[0]
    del hash_group[0]
    quad_word_group = [value for value in tokens_quadword_with_index if value[1] in [index[1] for index in hash_group]]
    quad_word_group.insert(0, first_value)
    quad_word_groups.append(quad_word_group)
    quad_word_group = []
  
  # return value = [['lead1', nword1, nword2, ...], ['lead2', nwordx1, nwordx2, ...], ...]
  return quad_word_groups


def make_stack_quadword_group(quadword_groups):
  # quadword_groups = [['lead1', nword1, nword2, ...], ['lead2', nwordx1, nwordx2, ...], ...]
  stack_quadword_group = []
  # print(quadword_groups)
  
  for quadword_group in quadword_groups:
    last_quadword_index = 0
    stacks = []
    stack = ''
    first_value = quadword_group[0]
    del quadword_group[0]
    i = 0
    while i < len(quadword_group):
      if i < 1 or stack == '':
        stack += quadword_group[i][0] + ' '
        if i == len(quadword_group) - 1:
            stacks.append(stack.rstrip())
        
      elif i >= 1:
        if len(stack.split(' ')) >= 4:
          stacks.append(stack.rstrip())
          stack = ''
          stack += quadword_group[i][0] + ' '
          last_quadword_index = quadword_group[i-1][1]
         
        elif quadword_group[i][0].split(' ')[2] == quadword_group[i-1][0].split(' ')[3]:
          stack += quadword_group[i][0].split(' ')[3] + ' '
          
          if last_quadword_index != 0:
            if quadword_group[i][1] > last_quadword_index and quadword_group[i][1] < last_quadword_index + 3:
              
              stack = stack.split(' ')
              del stack[0:3]
              stack = ' '.join(stack)
            
            
          if i == len(quadword_group) - 1:
            stacks.append(stack.rstrip())
            stack = ''

        else:
         
          if len(stack.split(' ')) < 4:
            stack = ''
          else:
            stacks.append(stack.rstrip())
            stack = ''
      
      # print(stacks)
      i += 1
    
    stacks.insert(0, first_value)
    stack_quadword_group.append(stacks)
      
      
  return stack_quadword_group




# --- ONE TO ONE
