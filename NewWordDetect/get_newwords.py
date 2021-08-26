import jieba.analyse
import pkuseg
import random
import os
import re
from model import TrieNode
import math
import time
from utils import load_dictionary,save_model,load_model
from collections import defaultdict
basedir = os.path.abspath(os.path.dirname(__file__))

seg = pkuseg.pkuseg(postag=True)

bad_words = ['且','是','涨', '跌', '于', '比', '年月', '可以', '再', '在','可能','仅', '吗', '这个', '这','致使', '包括', '很', '使', '加入', '逐渐', '之一', '年',
             '几乎','只','表示','或','以','上午','下午','两','盼望','指数','上调','为','内','同比','他','定期','开放','都','涨幅','报点','进行','缺乏','方面','月','股','将','最','也','主要','发布','岁','卖出','买入','渣打','等','达到','降低','减少','下跌','至','增多','回应','成为','增加','购买','超过','增长','达到','提高','升级','推动','折合','最低','最多','拥有','影响','起诉','下降','大跌','实现','侵权','上涨','通过','出售','质疑','扩张','显示']
good_pos = ['ns', 'n', 'vn', 'v', 'vn','nz','nt','un','l']  # 'nr' 人名

def seg_pos(line):
    line = line.strip('\n')
    cut_line = []
    index_dic = {}   # {1:(我,n),2:(爱,v)...}
    for i, item in enumerate(seg.cut(line)):
        cut_line.append(item[0])
        index_dic[i] = item

    seg_line = ' '.join(cut_line) # '我 爱 北京 天安门'
    assert len(index_dic) == len(cut_line), 'error,please check'
    return seg_line, index_dic


def get_keyword(seg_line):

    keywords1 = jieba.analyse.extract_tags(seg_line, topK=12, withWeight=True,
                                           allowPOS=('ns', 'n', 'vn', 'v', 'vn','nz','nt','un'))
    keywords2 = jieba.analyse.textrank(seg_line, topK=12, withWeight=True)
    keywords = []


    for item in keywords1:

        flag = 0
        for word in bad_words:
            if word in item[0]:
                flag = 1
        if flag != 1 and item[0]!=re.findall('[a-zA-Z]',item[0]):
            keywords.append(item[0])

    for item in keywords2:
        if item[0] in keywords:
            continue

        flag = 0
        for word in bad_words:
            if word in item[0]:
                flag = 1
        if flag != 1 and item[0]!=re.findall('[a-zA-Z]',item[0]):
            keywords.append(item[0])

    return keywords


def generate_ngram(seg_line,keywords,index_dic,n):
    dataline = seg_line.split(' ')

    word_index = defaultdict(list)
    for k, va in [(v, i) for i, v in enumerate(dataline)]:
        word_index[k].append(va)
    word_index = dict(word_index)    # the position of keyword in textline  {'熊猫':[5,7,11,16,26]...}


    results = []
    for key_word in keywords:
        indexs = word_index.get(key_word,-2)
        if indexs != -2:
            # if len(indexs) >= 8:
            #     indexs = random.sample(indexs, 7)   # performing downsample to keywords that appear too often
            for i in indexs:
                if i - 1 < 0:
                    pass
                else:
                    word = dataline[i - 1]
                    flag = 0
                    for item in bad_words:
                        if item == word:
                            flag = 1
                    if flag!=1 and index_dic[i - 1][1] in good_pos and word !=re.findall('[a-zA-Z]',word):
                        results.append(i - 1)   # choose the word in front of the keyword to create ngram, but such words should have good postags

                results.append(i)

                if i + 1 >= len(dataline):
                    pass
                else:
                    word = dataline[i + 1]
                    flag = 0
                    for item in bad_words:
                        if item == word:
                            flag = 1
                    if flag != 1 and index_dic[i][1] in good_pos and word !=re.findall('[a-zA-Z]',word):
                        results.append(i + 1)

    no_repeat_results = []
    [no_repeat_results.append(i) for i in results if not i in no_repeat_results]
    no_repeat_results = sorted(no_repeat_results)

    final_result = [dataline[i] for i in no_repeat_results]

    ngrams = []
    for i in range(1, n+1):
        ngrams.extend(zip(*[final_result[j:] for j in range(i)]))

    return ngrams


def gen_newword(line):
    seg_line, index_dic = seg_pos(line)
    keyword = get_keyword(seg_line)
    ngrams = generate_ngram(seg_line, keyword, index_dic, 2)

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

    for d in ngrams:
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


