# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 17:12:50 2018

@author: Philippe
"""

import requests
import re
from bs4 import BeautifulSoup
import nltk

class Presidents():

    def __init__(self, presidents):
        self.presidents = presidents

    def get_links(self):

        speeches_dict = {}
        for pr in self.presidents:

            url = 'https://millercenter.org/president/' + pr

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

            speeches_dict[pr] = speeches_links

        return speeches_dict

    def get_speeches(self, speeches_dict):

        speeches_pr = {}
        for pr in self.presidents:

            print('President Now: ', pr)
            speeches = {}
            for speech_link in speeches_dict[pr]:
                url_speech = requests.get(speech_link)
                html_speech = url_speech.text
                soup_speech = BeautifulSoup(html_speech, "html5lib")

                soup_text = soup_speech.find('div', {'class': 'transcript-inner'}).text

                link0 = 'https://millercenter.org/ \
                         the-presidency/presidential-speeches/'
                key = re.sub(link0, '',
                             speech_link)

                speeches[key] = soup_text

            speeches_pr[pr] = speeches

        return speeches_pr

    def tokenize(self, speeches_pr):

        tokens_pr = {}
        for pr in self.presidents:

            speeches = speeches_pr[pr]
            tokens_all = []
            for k, v in speeches.items():
                tokens = re.findall('\w+', speeches[k])
                for word in tokens:
                    tokens_all.append(word.lower())

            tokens_pr[pr] = tokens_all

        return tokens_pr

    def process_sw(self, tokens_pr, remove_from_sw = []):

        tokens_pr_ns = {}
        for pr in self.presidents:

            # Finally processing the words
            sw = nltk.corpus.stopwords.words('english')
            sw.append('applause')
            sw.append('Applause')
            # (Optional) Maintaining some stopwords
            for w in remove_from_sw:
                sw.remove(w)

            tokens_ns = []
            tokens_all = tokens_pr[pr]
            for word in tokens_all:
                if word not in sw:
                    tokens_ns.append(word)

            tokens_pr_ns[pr] = tokens_ns

        return tokens_pr_ns
