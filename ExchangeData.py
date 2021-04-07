import time
import requests
import json
import pandas as pd
import sys
from bs4 import BeautifulSoup as bs
import re
# from google.colab import files

def gettime():
    return int(round(time.time() * 1000))


def getResponse(url, headers, params):
    try:
        response = requests.request("GET", url, headers=headers, params=params)
        reqIsJson = False

        if "application/json" in response.headers.get('content-type'):
            reqIsJson = True

        if response.status_code == 200 and reqIsJson == True:
            return response

        if response.status_code == 200 and reqIsJson == False:
            print("Unsupported content type received : ", response.headers.get('content-type'))
            return response

        print('Status Code: ' + str(response.status_code))

        if response.status_code == 400:
            print("The server could not understand your request, check the syntax for your query.")
            print('Error Message: ' + str(response.json()))
        elif response.status_code == 401:
            print("Login failed, please check your user name and password.")
        elif response.status_code == 403:
            print("You are not entitled to this data.")
        elif response.status_code == 404:
            print("The URL you requested could not be found or you have an invalid view name.")
        elif response.status_code == 500:
            print("The server encountered an unexpected condition which prevented it from fulfilling the request.")
            print("Error Message: " + str(response.json()))
            print("If this persists, please contact customer care.")
        else:
            print("Error Message: " + str(response.json()))
    except:
        sys.exit()


def get_Shanghai_data(pages, gas_type):
    if gas_type == 'LNG':
        wareid = 3
    elif gas_type == 'pipeline':
        wareid = 6
    else:
        wareid = 6
    
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Referer': r'https://www.shpgx.com/html/gdtrqsj.html',
        'Connection': r'keep-alive',
        'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8'}
    s = requests.session()
    table = pd.DataFrame()
    for i in range(pages):
        params = {
            # 'wareid': 6, # for pipeline deals， 3 for LNG
            'wareid': wareid,  
            'cd': None,
            'starttime': None,
            'endtime': None,
            'start': 0 + 25 * i,
            'length': 25,
            'ts': str(gettime())}

        payload = {
            'wareid': 6,
            'cd': None,
            'starttime': None,
            'endtime': None,
            'start': 0,
            'length': 25,
            'ts': str(gettime())}

        # url = r'https://www.shpgx.com/html/gdtrqsj.html'
        url = r'https://www.shpgx.com/marketstock/dataList'
        response = s.get(url, headers=headers, params=params).text.encode('utf-8')
        # data = getResponse(url,headers, params).text.encode('utf8')
        data = pd.DataFrame(json.loads(response)['root'])
        rows = len(data.index)
        for i in range(rows):
            df = pd.DataFrame.from_dict(
                {'挂牌价': data.iloc[i]['basename'],
                 '成交价': data.iloc[i]['contprice'],
                 '价格单位':data.iloc[i]['priceunit'],
                 '挂牌量': data.iloc[i]['basenum'],
                 '成交量': data.iloc[i]['dealnum'],
                 '成交量单位': data.iloc[i]['countunit'],
                 '种类': data.iloc[i]['warekind'],
                 '交易方式': data.iloc[i]['ordmod'],
                 '开始日期': data.iloc[i]['startdate'],
                 '交收截至日': data.iloc[i]['enddate'],
                 '交收地': data.iloc[i]['jsd'],
                 '输入 时间': data.iloc[i]['createTime'],
                 '信息更新时间': data.iloc[i]['updateTime'],
                 '挂牌日期': data.iloc[i]['orderdate']}, orient='index')
            table = pd.merge(table, df, how='outer', left_index=True, right_index=True)
    return table.T

def get_Chongqing_pages(start_date, end_date):
    url = 'https://www.chinacqpgx.com/jyxx/index.php?type=0&area=&t1=' + str(start_date)+'&t2='+str(end_date)
    soup = bs(requests.get(url).text, features="lxml")
    page_codes = soup.find_all(name='div', attrs={'class': 'met_pager gm-pager'})[0]
    pages = int(re.findall('第/(\d*)页', page_codes.text)[0])
    return pages

# def get_shanghai_LNG_pages():
#     url = r'https://www.shpgx.com/html/yhtrqsj.html'
#     soup = bs(requests.get(url).text, features="lxml")
    
    
    
def get_Chongqing_data(start_date='20201207', end_date='20210114'):
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Referer': r'https://www.chinacqpgx.com/jyxx/index.php?type=0&area=&t1=20201201&t2=20201206',
        'Connection': r'keep-alive',
        'Cookie': r'Cookie: zero_areaArr3=%5B%22%E5%9B%9B%E5%B7%9D%22%2C%22%E5%8C%97%E4%BA%AC%22%2C%22%E9%87%8D%E5%BA%86%22%2C%22%E5%AE%81%E5%A4%8F%22%2C%22%E5%B9%BF%E5%B7%9E%22%2C%22%E9%9D%92%E6%B5%B7%22%2C%22%E5%8D%97%E5%AE%81%22%2C%22%E4%B8%8A%E6%B5%B7%22%2C%22%E5%86%85%E8%92%99%E5%8F%A4%22%2C%22%E4%BA%91%E5%8D%97%22%2C%22%E7%94%98%E8%82%83%22%2C%22%E6%96%B0%E7%96%86%22%2C%22%E9%99%95%E8%A5%BF%22%2C%22%E6%B9%96%E5%8D%97%22%2C%22%E8%B4%B5%E5%B7%9E%22%2C%22%E6%B1%9F%E8%A5%BF%22%2C%22%E6%B9%96%E5%8C%97%22%2C%22%E5%B9%BF%E8%A5%BF%22%2C%22%E5%90%89%E6%9E%97%22%2C%22%E8%BE%BD%E5%AE%81%22%2C%22%E5%A4%A9%E6%B4%A5%22%2C%22%E5%AE%89%E5%BE%BD%22%2C%22%E5%B9%BF%E4%B8%9C%22%2C%22%E5%B1%B1%E8%A5%BF%22%2C%22%E6%B1%9F%E8%8B%8F%22%2C%22%E6%B2%B3%E5%8C%97%22%2C%22%E5%B1%B1%E4%B8%9C%22%2C%22%E6%B2%B3%E5%8D%97%22%2C%22%E7%A6%8F%E5%BB%BA%22%2C%22%E5%85%A8%E4%B8%AD%E5%9B%BD%22%5D; Hm_lvt_f81598e2508cd3d34d620f5689165095=1610620639; Hm_lpvt_f81598e2508cd3d34d620f5689165095=1610620793'}
    pages = get_Chongqing_pages(start_date, end_date)
    page_data = pd.DataFrame()
    for i in range(1, pages + 1):
        params = {
            'type': 'all',
            'area': None,
            't1': start_date,
            't2': end_date,
            'p': i
        }
        url = r'https://www.chinacqpgx.com/jyxx/index.php'
        s = requests.session()
        table = pd.DataFrame()
        # response = s.get(url, headers=headers, params=params).text.encode('utf-8')
        response = s.get(url, headers=headers, params=params)
        soup = bs(response.text, features='lxml')
        code = soup.find_all(name='div', attrs={'class': 'trade-content'})[0].find_all('li')
        rows = len(code) - 6

        for i in range(rows):
            row_data = pd.DataFrame.from_dict({
                code[0].text: code[6 + i].text.splitlines()[2],
                code[1].text: code[6 + i].text.splitlines()[3],
                code[2].text: code[6 + i].text.splitlines()[4],
                code[3].text: code[6 + i].text.splitlines()[5],
                code[4].text: code[6 + i].text.splitlines()[6],
                code[5].text: code[6 + i].text.splitlines()[7]

            }, orient='index')
            page_data = pd.merge(page_data, row_data, how='outer', left_index=True, right_index=True)
    return page_data.T


def main():
    ChongQing_data = get_Chongqing_data('20210315','20210401')
    ChongQing_data.to_excel('Chongqing data.xlsx')
    # files.download('Chongqing data.xlsx')
    

    Shanghai_data_LNG = get_Shanghai_data(1,'LNG')
    Shanghai_data_LNG.to_excel('shanghai LNG data.xlsx')
    # files.download('shanghai LNG data.xlsx')
    
    Shanghai_data_pipeline = get_Shanghai_data(1,'pipeline')
    Shanghai_data_pipeline.to_excel('shanghai pipeline data.xlsx')
    # files.download('shanghai pipeline data.xlsx')
    
if __name__ == '__main__':
    main()
