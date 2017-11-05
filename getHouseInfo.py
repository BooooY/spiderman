# encoding='utf-8'
import requests
from bs4 import BeautifulSoup 

def getHouseInfo(page_num):
    url = 'http://shenzhen.qfang.com/garden/n' + '{}'.format(page_num)
    data = requests.get(url)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text,'lxml')
    houseinfo = {}
    houseinfo['小区名称'] = [i.text.strip() for i in soup.select('.house-title a')]   #搜寻小区名称（一页纳入列表）
    houseinfo['小区地址'] = [i.select('p')[2].select('span')[0].text for i in soup.select('.show-detail')] #搜寻小区位于的大区（一页纳入列表）
    houseinfo['小区id'] = [i['href'].lstrip('/garden/desc/') for i in soup.select('.house-title a')] #搜寻小区的链接id
    return houseinfo

def getTransctionInfo(name,location,href_id):
    url = 'http://shenzhen.qfang.com/garden/desc/'+ href_id #获取二手房小区分页链接
    data = requests.get(url)
    soup = BeautifulSoup(data.text,'lxml') #获取二手房小区分页信息
    page_num = soup.select('.turnpage_num a')[-1].text #获取二手房成交信息分页数  
    transinfo_url = 'http://shenzhen.qfang.com/garden/transactiondata/'+ href_id + '/' #二手房成交链接
    transdata1 = requests.get(transinfo_url+'1') #获取第一页成交信息
    transinfo_soup1 = BeautifulSoup(transdata1.text,'lxml')
    transdata2 = requests.get(transinfo_url+page_num) #获取最后一页成交信息
    transinfo_soup2 = BeautifulSoup(transdata2.text,'lxml')
    data_list = {}
    data_list['小区名称'] = ['{}'.format(name)]
    print(data_list['小区名称'])
    data_list['小区地址'] = ['{}'.format(location)]
    data_list['建筑年代'] =[soup.select('.link')[0].text]
    data_list['最近一套的面积'] = [transinfo_soup1.select('.the-second')[1].text]
    data_list['最近一套的成交总价'] = [transinfo_soup1.select('.the-fourth')[1].text]
    data_list['最近一套的成交时间'] = [transinfo_soup1.select('.the-third')[1].text]
    data_list['最近一套的成交单价'] = [transinfo_soup1.select('.the-fifth')[1].text.strip('元/m²')]
    data_list['最早一套的面积'] = [transinfo_soup2.select('.the-second')[-1].text]
    data_list['最早一套的成交总价'] = [transinfo_soup2.select('.the-fourth')[-1].text]
    data_list['最早一套的成交时间'] = [transinfo_soup2.select('.the-third')[-1].text]
    data_list['最早一套的成交单价'] = [transinfo_soup2.select('.the-fifth')[-1].text.strip('元/m²')]    
    return data_list

def getPageNum(): #获取二手房主页面的列表分页数
    url = 'http://shenzhen.qfang.com/garden/'
    data = requests.get(url)
    soup = BeautifulSoup(data.text,'lxml') 
    page_num = soup.select('.turnpage_num a')[-1].text.strip()
    page_num = int(page_num)
    return page_num
getPageNum()


def init():
    data_total ={}
    for i in range(1,2):
        for j in range(1,20):
            house = getTransctionInfo(getHouseInfo(i)['小区名称'][j],getHouseInfo(i)['小区地址'][j],getHouseInfo(i)['小区id'][j])
            data_total = dict(data_total,**house)
            print(house)
            print(data_total)
init()
import pandas as pd
# df = pd.DataFrame(data_total)
# df
