# -*- coding: utf-8 -*-
import pickle
import os

from model import TrieNode


from collections import defaultdict
basedir = os.path.abspath(os.path.dirname(__file__))

def gen_newword(ngram):

    root_name = basedir + "/data/root.pkl"
    if os.path.exists(root_name):
        root = load_model(root_name)
    else:
        dict_name = basedir + '/data/dict.txt'
        word_freq = load_dictionary(dict_name)
        root = TrieNode('*', word_freq)
        save_model(root, root_name)

    # dict_name = basedir + '/data/dict.txt'
    # word_freq = load_dictionary(dict_name)
    # root = TrieNode('*', word_freq)

    for d in ngram:
        root.add(d)

    topN = 4
    add_word = root.find_word(topN)

    results= []
    x = []
    for word, score in add_word.items():
        results.append(word)
        x.append((word,score))
    for item in x:
        print(item[0],'---',item[1])
    return results



def load_dictionary(filename):
    word_freq = {}
    print('------> 加载外部词集')
    with open(filename, 'r',encoding='utf-8') as f:
        for line in f:
            try:
                line_list = line.strip().split(' ')
                # 规定最少词频
                if int(line_list[1]) > 2:
                    word_freq[line_list[0]] = line_list[1]
            except IndexError as e:
                print(line)
                continue
    return word_freq

def save_model(model, filename):
    with open(filename, 'wb') as fw:
        pickle.dump(model, fw)


def load_model(filename):
    with open(filename, 'rb') as fr:
        model = pickle.load(fr)
    return model

def write_to_file(name,data):
    with open('data/{}.txt'.format(name),'a',encoding='utf-8') as f:
        for item in data:
            f.write(str(item))
            f.write('\n')




