# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 11:55:21 2018

@author: Philippe

Obama vs Trump
"""
# %%
import requests
import re
from bs4 import BeautifulSoup
import nltk

president = 'truman'
url = 'https://millercenter.org/president/' + president

r_1 = requests.get(url)
html_1 = r_1.text
soup_1 = BeautifulSoup(html_1, "html5lib")

view_speeches = str(soup_1.findAll('a', string = 'View His Speeches'))
view_speeches = str(re.findall(r'"(.*?)"', view_speeches)[0])

# For Trump's different URL
initial = 'https://millercenter.org'
if view_speeches[0:24] != initial:
    view_speeches = initial + view_speeches

r_2 = requests.get(view_speeches)
html_2 = r_2.text
soup_2 = BeautifulSoup(html_2, "html5lib")

speeches_links = str(soup_2.findAll('div', {'class': 'views-row'}))
speeches_links = re.findall(r'href="(.*?)"', speeches_links)
speeches_links = [(initial + i) for i in speeches_links]

# %% All Speeches of 1 president
speeches = {}
for speech_link in speeches_links:
    url_speech = requests.get(speech_link)
    html_speech = url_speech.text
    soup_speech = BeautifulSoup(html_speech, "html5lib")

    soup_text = soup_speech.find('div', {'class': 'transcript-inner'}).text

    key = re.sub('https://millercenter.org/the-presidency/presidential-speeches/', '',
                 speech_link)

    speeches[key] = soup_text

# %% Concatenating and Tokenizing All Speeches
tokens_all = []
for k, v in speeches.items():
    tokens = re.findall('\w+', speeches[k])
    for word in tokens:
        tokens_all.append(word.lower())

# Finally processing the words
sw = nltk.corpus.stopwords.words('english')
sw.append('applause')
sw.remove('i')
sw.remove('me')

tokens_ns = []
for word in tokens_all:
    if word not in sw:
        tokens_ns.append(word)

# %% Plotting

#import matplotlib.pyplot as plt
import seaborn as sns

# Figures inline and set visualization style
sns.set()

# Create freq dist and plot
freqdist1 = nltk.FreqDist(tokens_ns)
freqdist1.plot(25)
