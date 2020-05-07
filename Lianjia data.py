import requests
import re
import pandas as pd
from bs4 import BeautifulSoup as bs



def GetPages(url, headers, cookies):
    text = requests.get(url, headers=headers, cookies = cookies).text
    soup = bs(text)
    pages = re.findall('<a href="/ershoufang/pg2c1111027382441rs国际城" data-page="2">2</a>')

def PriceInfo(url,headers, cookies):
    text = requests.get(url, headers=headers, cookies = cookies).text
    soup = bs(text)
    rooms =[i.text.strip().split('|')[0] for i in soup.findAll(name='div', attrs={'class':'houseInfo'})]
    area = [float(i.text.strip().split('|')[1][:-3]) for i in soup.findAll(name='div', attrs={'class':'houseInfo'})]
    direction = [i.text.strip().split('|')[2] for i in soup.findAll(name='div', attrs={'class':'houseInfo'})]
    decoration = [i.text.strip().split('|')[3] for i in soup.findAll(name='div', attrs={'class':'houseInfo'})]
    floor = [i.text.strip().split('|')[4] for i in soup.findAll(name='div', attrs={'class':'houseInfo'})]
    year = [int(i.text.strip().split('|')[5][:-3].strip()) for i in soup.findAll(name='div', attrs={'class':'houseInfo'})]
    buildingtype = [i.text.strip().split('|')[6] for i in soup.findAll(name='div', attrs={'class':'houseInfo'})]
    price = [float(i.text[:-1]) for i in soup.findAll(name = 'div', attrs={'class':'totalPrice'})]
    block =[i.text.strip() for i in soup.findAll(name='a', attrs={'data-el':'region'})]
    return pd.DataFrame({'block':block,'rooms':rooms, 'area':area, 'price':price, 'direction':direction,'decoration':decoration,'floor':floor, 'year':year, 'building type':buildingtype})

def main():
    url = r'https://bj.lianjia.com/ershoufang/c1111027382441rs%E5%9B%BD%E9%99%85%E5%9F%8E/'

    headers ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
    cookies ={'Cookie': 'BAIDUID=A467EBC2C2D0C1F5CE71C86F2D851B89:FG=1; PSTM=1569895226; BIDUPSID=9BD73512109ADEBC79D0E6031A361FF2; ab_jid=3401447befc2a1f1fb58e1332e7a70a45049; ab_jid=3401447befc2a1f1fb58e1332e7a70a45049; ab_jid_BFESS=3401447befc2a1f1fb58e1332e7a70a45049; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598'}

    Price = PriceInfo(url,headers,cookies)
    with pd.ExcelWriter('Lianjia info.xlsx') as Writer:
        Price.to_excel(Writer, sheet_name = 'Lianjia')

if __name__ == '__main__':
    main()
