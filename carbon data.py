import pandas as pd 
# import numpy as np 
# import matplotlib.pyplot as plt 
import requests
import re
import time
from bs4 import BeautifulSoup as bs
from datetime import datetime


def make_soup(url, payload):
    # parse a html page for analysi with bs4
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
    cookies = {
        'Cookie': 'BAIDUID=A467EBC2C2D0C1F5CE71C86F2D851B89:FG=1; PSTM=1569895226; BIDUPSID=9BD73512109ADEBC79D0E6031A361FF2; ab_jid=3401447befc2a1f1fb58e1332e7a70a45049; ab_jid=3401447befc2a1f1fb58e1332e7a70a45049; ab_jid_BFESS=3401447befc2a1f1fb58e1332e7a70a45049; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598'}
    text = requests.get(url, headers=headers, cookies=cookies,params=payload).text
    soup = bs(text, features='lxml')
    return soup


def table_extractor(url, payload):
    soup = make_soup(url,payload)
    location = re.findall('"housetext":"(.*?)","indate"', str(soup))
    date = re.findall('"indate":"(.*?)","indateStr"', str(soup))
    low = re.findall('"low":(.*?),"open"', str(soup))
    open_price = re.findall('"open":(.*?),"remark"', str(soup))
    Type= re.findall('"subTypeName":"(.*?)"', str(soup))
    average= re.findall('"average":(.*?),"close"', str(soup))
    close= re.findall('"close":(.*?),"dataid"', str(soup))
    deal= re.findall('"deal":(.*?),"dealamount"', str(soup))
    dealamount= re.findall('"dealamount":(.*?),"dealnum"', str(soup))
    dealnum= re.findall(',"dealnum":(.*?),"high"', str(soup))
    high= re.findall('"high":(.*?),"houseid"', str(soup))
    
    table = pd.DataFrame({'交易所':location,
                          '交易类型':Type,
                          '交易日期':date,
                          '开盘价（元）':open_price,
                          '收盘价（元）':close,
                          '最低价（元）':low,
                          '最高价（元）':high,
                          '平均价（元）':average,
                          '成交价（元）':deal,
                          '交易额（元）':dealamount,
                          '交易量（吨）':dealnum
                          }
                          )
    return table


def combined_table(url,total_page):
    Data = pd.DataFrame()
    
    for page in range(1,total_page+1):
        timestamp = str(int(datetime.timestamp(datetime.now())*1000))
        payload = {
        'jsoncallback': 'jQuery1112009284790594066039_1627985108915',
        'lcnK': 'f57f50a55dc99564468dba987810aaff',
        'brand': 'TAN',
        'page': str(page),
        'rows': '50',
        '_': timestamp
        }
        table = table_extractor(url,payload)
        Data= Data.append(table)
    return Data
    
def WriteToExcel(name, dataframe):
    '''
    Parameters:
    name = name of the spreadsheet
    dataframe = dataframe to be written into the excel spreadsheet
    Write dataframes into excel
    '''
    filename = name+' '+ time.ctime().replace(':',' ')
    with pd.ExcelWriter(filename+'.xlsx') as writer:
        dataframe.to_excel(writer, sheet_name = name)


def main():
    entry_page  = r'http://k.tanjiaoyi.com/#l'
    url = r'http://k.tanjiaoyi.com:8080/KDataController/datumlist4Embed.do'
    total_page = 420 #change the total page for how many pages you want (50 rows per page)
    Data = combined_table(url,total_page)
    WriteToExcel('Carbon data',Data) 

if __name__ == '__main__':
    main()

  
    