from nltk import ngrams
import re
import string

def filterText(text):
  filter_text = text.replace('\n', ' ').replace('?','').lower()
  remove_extra_spaces = re.sub(' +', ' ', filter_text)

  return ''.join(x for x in remove_extra_spaces if x in string.printable)



def createTokens(text):
  n = 4
  n_grams = ngrams(text.split(), n)
  
  # print(len(text))
  tokens = []
  for grams in n_grams:
    
    n_word = ''
    for gram in grams:
      n_word += gram + ' '; 

    n_word = n_word.rstrip()
    tmp = (n_word)
    tokens.append(tmp)

  return tokens
  

