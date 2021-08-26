

from utils import gen_newword

import time
import os
import json
from tqdm import tqdm
basedir = os.path.abspath(os.path.dirname(__file__))
words = []


with open('data/news_data_unseg1000.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()

file = open('data/ngrams.json', 'r', encoding='utf-8')
ngrams = json.loads(file.read())

with open('data/newwordsall.txt', 'a', encoding='utf-8') as f:
    for i, line in enumerate(data):
        #print('···generating newwords···')
        start = time.time()

        newwords = gen_newword(ngrams[i])
        end = time.time()
        print(end-start,'s')
        for word in newwords:
            f.write(word)
            f.write('\n')


