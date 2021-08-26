from multiprocessing import Process
from time import sleep
from tqdm import tqdm
import requests
from lxml import etree


headers = {
    'Cookie':'BIDUPSID=5591A60BC9B0AD23308854BE84D7582E; PSTM=1625021986; BD_UPN=12314753; __yjs_duid=1_821d2981fd666aee500678e614cc18471625127398093; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=34268_33801_33967_34224_31253_34004_34113_26350_34092; delPer=0; BD_CK_SAM=1; PSINO=6; sug=3; sugstore=0; ORIGIN=0; bdime=0; BAIDUID=5591A60BC9B0AD23853C6FF55AB46C55:SL=0:NR=10:FG=1; BAIDUID_BFESS=5591A60BC9B0AD23853C6FF55AB46C55:SL=0:NR=10:FG=1; H_PS_645EC=f28cDlAinIPEd8LkwHdMlLkUf6QUL%2FdFTeKifo8UuWEmUBRCpFNchQFt6ig; BA_HECTOR=a4200h008g8ka185ls1geoen10r',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def getagent():
    url = "http://api.hailiangip.com:8422/api/getIp?type=1&num=1&pid=&unbindTime=60&cid=&orderId=O21071716165004538716&time=1626849527&sign=668db411d8c2ac709b01688d589130ba&noDuplicate=1&dataType=0&lineSeparator=0&singleIp="


def obj(text,fail_spider_words):
        data = []

        url = f'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd={text}&rn=20&oq=%25E5%25AE%259D%25E7%2587%2583%25E7%259B%259B%25E5%25A4%25A7&rsv_pq=8673684f0001b3d6&rsv_t=e1d7eZfSWw5zq5HfPEvp%2BdayKYofuiWNAqmAmAKEf6H5DSN%2Fl4AEXEIZL8g&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t'

        res =requests.get(url,headers=headers).text
        ex = etree.HTML(res)
        for i in range(1,11):
            title = ex.xpath(f'//*[@id="{i}"]/h3/a//text()')
            if len(''.join(title).replace('\n','')) != 0:
                u = ''.join(title).replace(' ', '').replace('\n','')
                data.append(u)
        if data==[]:
            sleep(1.5)
            #print(f"{text} 请求数据为空，重新爬取")
            res = requests.get(url, headers=headers).text
            ex = etree.HTML(res)
            for i in range(1, 11):
                title = ex.xpath(f'//*[@id="{i}"]/h3/a//text()')
                if len(''.join(title).replace('\n', '')) != 0:
                    u = ''.join(title).replace(' ', '').replace('\n', '')
                    if '视频大全' in u:
                        continue
                    if '百度图片' in u:
                        continue
                    if '的最新相关信息' in u:
                        continue
                    if '知乎' in u:
                        continue
                    if '百度地图' in u:
                        continue
                    if '百度爱采购' in u:
                        continue
                    data.append(u)
        if data==[]:
            fail_spider_words.append(text)
            print(f"{text} 爬取仍然为空，已存入记下")


        result = (text,data)
        # spider_result.append(result)
        return result


# text = '四环生物'
# print(obj(text))



