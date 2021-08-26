# -*- coding: utf-8 -*-
import pandas as pd
import re
from spider.spider import obj

def select(newwords,fail_spider_words,spider_result,positive_words,negative_words):
    for item in newwords:
        result = obj(item,fail_spider_words)
        if result[1] == []:
            continue
        spider_result.append(result)  # save spider result
        word,score = mark_scores(result)

        if score>=4000:
            positive_words.append(word)
            return word
        if score<=-4000:
            negative_words.append(word)




def mark_scores(result):
    score = 0
    word = result[0]
    titles = result[1]
    whole_count = 0
    part_count = 0

    if word == '孚生物':
        score -= 100
    if word == '胜生物':
        score -= 100
    # if word == '政府补助':
    #     score -= 3000
    # if word == '智能配送':
    #     score -= 3000
    for title in titles:
        if str('\''+ word + '-百度百科'+'\'') == title:
            score -= 5000
        if word in title and '百度百科' in title and '公司' in title:
            score += 5000

        if '的意思' in title:
                score -= 100
        if '是什么意思' in title:
                score -= 100

        if word not in title:
            whole_count += 1
        # for item in jieba.lcut(word):
        #     if item in title:
        #         part_count += 1

        if str('\''+ word + '-百度百科'+'\'') == title and 'MBA智库百科' in title:
            word = ''.join(title.replace('-MBA智库百科',''))
            score += 5000

    score -= int((whole_count / (len(titles) + 1)) * 30)
    # score += int((part_count/len(titles))*6)

    return word,score


with open('data/newwords10.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        word = line.strip('\n')

# no_repeat_words = []
# [no_repeat_words.append(i) for i in final_words if not i in no_repeat_word
'idf高的去掉 v+介词去掉  归一化？ 熊猫互娱出现太多 没有熊猫直播'


