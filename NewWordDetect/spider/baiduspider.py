#encoding:utf-8
import requests
import os
import fake_useragent
from bs4 import BeautifulSoup
import threading
import csv

GLOCK = threading.Lock()


urllist = []
keylist = []


def get_useragent():
    location = os.getcwd() + '/fake_useragent.json'
    ua = fake_useragent.UserAgent(path=location)
    return ua.random


def baiduSpider():
    while True:
        GLOCK.acquire()
        if len(urllist) == 0 and len(keylist) == 0:
            GLOCK.release()
            break
        if len(urllist) > 0:
            infos = urllist.pop()
        else:
            infos = ''

        GLOCK.release()

        if infos:

            headers = {
                'user-agent': get_useragent()
            }
            tunnel = "tps109.kdlapi.com:15818"
            # 用户名密码方式
            username = "t12687239577646"
            password = "rtvpweqv"
            proxies = {
                "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
                "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
            }

            try:
                url = infos[-1]
                response = requests.get(url, headers=headers,proxies=proxies)
            except:
                # print(infos[-1],'请求错误！')
                urllist.insert(0,infos)
            else:
                response.encoding = response.apparent_encoding
                html = BeautifulSoup(response.content, 'lxml')
                content = html.find_all('h3', class_="t")
                titleList = []
                for ct in content:
                    title = str(ct.text).replace('\n','').replace(' ', '')
                    titleList.append(title)
                if titleList ==[]:
                    print(f"{url} 请求数据为空，重新插入列表")
                    urllist.insert(0, url)
                else:
                    datas = [infos[0],titleList]
                    saveCsv("80-90w-spider", datas)

def saveCsv(filename,content):
    "保存数据为CSV文件"
    fp = open(f'{filename}.csv', 'a+', newline='', encoding='utf-8-sig')
    csv_fp = csv.writer(fp)
    csv_fp.writerow(content)
    fp.close()
    print(f"写入了{content}")


def writeFile(filename,content):
    with open(f'{filename}.txt','a+',encoding='utf-8') as f:
        f.write(str(content)+'\n')
        f.close()
    print(f"{content} 写入文件中")


def readFile():
    with open('80-90w.txt','r',encoding='utf-8') as f:
        data = f.read().split('\n')
        for d in data:
            if d != "":
                keylist.append(d)

def keyurls():
    while True:
        GLOCK.acquire()
        if len(keylist) == 0:
            GLOCK.release()
            break
        keywords = keylist.pop()
        GLOCK.release()
        weburl = f"https://www.baidu.com/s?wd={keywords}"
        infos = [keywords,weburl]
        urllist.append(infos)



def run():

    readFile()
    for i in range(100):
        th = threading.Thread(target=keyurls)
        th.start()

    for i in range(10):
        th = threading.Thread(target=baiduSpider)
        th.start()


if __name__ == '__main__':
    run()