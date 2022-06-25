from nltk import ngrams
import hashlib
import re

def filterText(text):
  filter_text = text.replace('\n', ' ').replace('?','').lower()
  # print(re.sub(' +', ' ', filter_text))
  return re.sub(' +', ' ', filter_text)

def createTokens(text):
  n = 4
  n_grams = ngrams(text.split(), n)
  
  # print(len(text))
  tokens = []
  for i, grams in enumerate(n_grams):
    
    n_word = ''
    for index, gram in enumerate(grams):
      n_word += gram + ' '; 

    n_word = n_word.rstrip()
    tmp = (n_word, i)
    tokens.append(tmp)

  return tokens
  
def createHashesMD5(tokens):
  hashes = []

  for token in tokens:
    hashing = hashlib.md5(token[0].encode())
    hashing = hashing.hexdigest() # menghasilkan 32 huruf dan angka
    # print(hashing)
    hashes.append((hashing, token[1]))

  return hashes
