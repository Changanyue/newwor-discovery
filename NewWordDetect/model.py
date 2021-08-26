# -*- coding: utf-8 -*-

import math
import json
import time
import random
file= open('data/bigram_freq.json', 'r', encoding='utf-8')
freq_dic = json.loads(file.read())
N = len(freq_dic)

class Node(object):
    """
    建立字典树的节点
    """
    def __init__(self, char):
        self.char = char
        # 记录是否完成
        self.word_finish = False
        # 用来计数
        self.count = 0
        # 用来存放节点
        self.child = []


class TrieNode(object):
    """
    建立前缀树，并且包含统计词频，计算互信息、idf的方法
    """

    def __init__(self, node, data=None, PMI_limit=20):
        """
        初始函数，data为外部词频数据集
        """
        self.root = Node(node)
        self.PMI_limit = PMI_limit
        if not data:
            return
        node = self.root
        for key, values in data.items():
            new_node = Node(key)
            new_node.count = int(values)
            new_node.word_finish = True
            node.child.append(new_node)

    def add(self, word):

        node = self.root  # 根结点*
        # 正常加载
        for count, char in enumerate(word):
            # word: ('能源', '汽车'),  count,char: 0 能源, 1 汽车
            found_in_child = False
            # 在节点中找字符
            for child in node.child:
                if char == child.char:
                    node = child
                    found_in_child = True
                    break

            # 顺序在节点后面添加节点。 a->b->c
            if not found_in_child:
                new_node = Node(char)
                node.child.append(new_node)  # 根结点添加子结点char
                node = new_node

            # 判断是否是ngram中的最后一个节点，这个词每出现一次就+1
            if count == len(word) - 1:
                node.count += 1
                node.word_finish = True


    def search_one(self):
        """
        计算互信息: 寻找一阶共现，并返回词概率
        """
        result = {}
        node = self.root
        if not node.child:
            return False, 0

        # 计算 1 gram 总的出现次数
        total = 0
        for child in node.child:
            if child.word_finish is True:
                total += child.count

        # 计算 当前词 占整体的比例
        for child in node.child:
            if child.word_finish is True:
                result[child.char] = (child.count / total, child.count)

        return result, total

    def search_bi(self):
        """
        计算互信息: 寻找二阶共现，并返回 log2( P(X,Y) / (P(X) * P(Y)) 和词概率
        """
        result = {}
        node = self.root
        if not node.child:
            return False, 0

        total = 0  # 2 gram的total 用来计算P(x,y)
        one_dict, total_one = self.search_one()  # 1 gram 各词的占比，和 1 gram 的总次数
        for child in node.child:
            for ch in child.child:
                if ch.word_finish is True:
                    total += ch.count  # a_b 共同出现的次数

        for child in node.child:
            for ch in child.child:
                if ch.word_finish is True:
                    # 互信息值越大，说明 a,b 两个词相关性越大
                    Count_xy = max(ch.count, 1)
                    Pxy = Count_xy / total
                    Px = one_dict[child.char][0]
                    Py = one_dict[ch.char][0]
                    Count_x = one_dict[child.char][1]
                    Count_y = one_dict[ch.char][1]

                    PMI = math.log(max(ch.count, 1), 2) - math.log(total, 2) - math.log(Px,2) - math.log(Py,2)
                    # nodict PMI = math.log(Count_xy, 2) + math.log(total, 2) - math.log(Count_x, 2) - math.log(Count_y, 2)
                    EMI = math.log(Count_xy, 2) - math.log(Count_x,2) - math.log(Count_y, 2) + math.log(total, 2)

                    result[child.char + '_' + ch.char] = (PMI, ch.count / total)

        return result


    def find_word(self, N):
        # 通过搜索得到互信息
        # 例如: dict{ "a_b": (PMI, 出现概率), .. }
        bi = self.search_bi()

        result = {}
        for key, values in bi.items():
            d = "".join(key.split('_'))
            idf = freq_dic.get(d,0)/1000

            # 计算公式 score = PMI - IDF
            try:
                result[key] = (values[0]) * values[1] #- idf

            except KeyError as err:
                print('error:{}'.format(err))

        # 按照 大到小倒序排列，value 值越大，说明是组合词的概率越大
        # result变成 => [('世界卫生_大会', 0.4380419441616299), ('蔡_英文', 0.28882968751888893) ..]
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)

        try:
            dict_list = [result[0][0]]
        except IndexError as err:
            print('error:{}'.format(err))


        add_word = {}
        new_word = "".join(dict_list[0].split('_'))
        # 获得概率
        add_word[new_word] = result[0][1]
        #add_word[new_word] = r2[0][1]

        for d in result[1: N]:
            flag = True
            for tmp in dict_list:
                pre = tmp.split('_')[0]
                # 新出现单词后缀，再老词的前缀中 or 如果发现新词，出现在列表中; 则跳出循环 
                # 前面的逻辑是： 如果A和B组合，那么B和C就不能组合(这个逻辑有点问题)，例如：`蔡_英文` 出现，那么 `英文_也` 这个不是新词
                # 疑惑: **后面的逻辑，这个是完全可能出现，毕竟没有重复**
                if d[0].split('_')[-1] == pre or "".join(tmp.split('_')) in "".join(d[0].split('_')):
                    flag = False
                    break
            if flag:
                new_word = "".join(d[0].split('_'))
                add_word[new_word] = d[1]
                dict_list.append(d[0])

        return add_word
