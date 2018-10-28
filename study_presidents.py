# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 18:16:44 2018

@author: Philippe
"""

import nltk
import pandas as pd

from presidents_class import Presidents

# Using the Class
p_list = ['trump', 'obama', 'gwbush', 'clinton', 'bush', \
          'reagan', 'carter', 'ford', 'nixon', 'lbjohnson', \
          'kennedy', 'eisenhower']
          # The rest is not working...
          # 'truman', 'fdroosevelt', 'hoover', \
          # 'coolidge', 'harding', 'wilson', 'taft', 'roosevelt']
          # 'mckinley', 'cleveland', 'bharrison', 'arthur', 'garfield', \
          # 'hayes', 'grant', 'johnson', 'lincoln', 'buchanan', \
          # 'pierce', 'fillmore', 'taylor', 'polk', 'tyler', 'harrison', \
          # 'vanburen', 'jackson', 'jqadams', 'monroe', 'madison', \
          # 'jefferson', 'adams', 'washington']

presidents = Presidents(p_list)

speeches_links = presidents.get_links()

speeches = presidents.get_speeches(speeches_links)
for key,_ in speeches.items():
    list_speeches = []
    for k,_ in speeches[key].items():
        list_speeches.append(speeches[key][k])
    df = pd.DataFrame(list_speeches)
    df.to_csv(key + '_speeches.csv', sep = ',')

token_speeches = presidents.tokenize(speeches)
for k,v in token_speeches.items():
    df = pd.DataFrame(token_speeches[k])
    df.to_csv(k + '_token_speeches.csv', sep = ',')

token_speeches_no_sw = presidents.process_sw(token_speeches,
                                             remove_from_sw = ['i'])
for k,v in token_speeches_no_sw.items():
    df = pd.DataFrame(token_speeches_no_sw[k])
    df.to_csv(k + '_token_speeches_no_sw.csv', sep = ',')

# Plotting
import matplotlib.pyplot as plt
import seaborn as sns

# Figures inline and set visualization style
sns.set()

freqdist = {}
for k,_ in token_speeches_no_sw.items():
    freqdist[k] = dict(nltk.FreqDist(token_speeches_no_sw[k]))
    
freqdist_sorted = {}
for k,_ in freqdist.items():
    freqdist_sorted[k] = sorted(freqdist[k], 
                                key=freqdist[k].get, 
                                reverse=True)

x = {}
y = {}
for key,_ in freqdist_sorted.items():
    x[key] = []
    y[key] = []
    for k in freqdist_sorted[key]:
        x[key].append(k)
        y[key].append(freqdist[key][k])
            
for k in ['trump', 'obama', 'reagan', 'carter']:
    plt.scatter(x[k][:21], y[k][:21], label = k)
plt.legend()
plt.xticks(rotation=90)
plt.title('Word Frequency for Different Presidents')
plt.ylabel('# of Occurrences')
plt.show()
plt.savefig('wordfreq.jpg')
plt.close()
        
# Bigrams
import random

def CreateTuples(words):
   tuples = []
 
   for i in range(len(words)-1):
      tuples.append((words[i], words[i+1]))
 
   return tuples

def sent_gen(cfdist, len_sent = 20, max_like = False):
   word = 'i'
   sentence = []
   sentence.append(word)
 
   while len(sentence) < len_sent:
      options = []
      for gram in cfdist[word]:
         for result in range(cfdist[word][gram]):
            options.append(gram)
            
      if max_like == False:
          word = options[int((len(options))*random.random())]
      else:
          word = options[0]
      sentence.append(word)
 
   return sentence

tuples = {k:CreateTuples(token_speeches[k]) for k,_ in token_speeches.items()}

cfdist = {k:nltk.ConditionalFreqDist(tuples[k]) for k,_ in tuples.items()}
        
sentences = {k:sent_gen(cfdist[k], 
                        len_sent = 20,
                        max_like = False) for k,_ in cfdist.items()}








        