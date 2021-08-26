import re

bad_words = ['经ai','a股','本次','快讯','和', '及', '每','认为','报道','等','达到','降低','减少','下跌','至','增多','回应','成为','增加','购买','超过','增长','达到','提高','升级','推动','折合','最低','最多','拥有','影响','起诉','下降','大跌','实现','侵权','上涨','通过','出售','质疑','扩张','显示']

def get_stopwords():
    with open('C:/Users/fffanzhang/Desktop/newwords/data/stopwords.txt', 'r',encoding='utf-8') as f:
        stopword = [line.strip() for line in f]
    return set(stopword)


with open('data/news_data_unseg.txt', 'r',encoding='utf-8') as f:
    data = f.readlines()
with open('data/news_data_process.txt', 'a', encoding='utf-8') as f:
    for line in data:

        en = re.findall('[.0-9a-zA-z]', line)
        for item in en:
            if item != '5g':
                line = line.replace(item, '')

        p1 = re.compile(r'[(](.*?)[)]', re.S)
        s1 = re.findall(p1, line)
        for item in s1:
            kuohao1 = '(' + item + ')'
            line = line.replace(kuohao1, '')

        p2 = re.compile(r'[（](.*?)[）]', re.S)
        s2 = re.findall(p2, line)

        for item in s2:
            kuohao2 = '（' + item + '）'
            line = line.replace(kuohao2, '')

        percent = re.findall('[.0-9%]', line)
        for item in percent:
            line = line.replace(item, '')

        money = re.findall('[.0-9亿美日元]', line)
        for item in money:
            line = line.replace(item, '')

        date = re.findall('[年月]', line)
        for item in date:
            line = line.replace(item, '')


        for item in bad_words:
            line = line.replace(item, '')

        stopwords = get_stopwords()
        for item in stopwords:
            line = line.replace(item, '')
        line = line.replace('，','').replace('。','').replace('、','')


        f.write(line)