# encoding = 'utf-8'
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import csv
# import time

def getHouseInfo():   #获取各小区的概要信息（小区名称、地址、ID等）
    houseinfo = {}
    page_num=getPageNum() #获取主页面列表的分页数
    for i in range(1,page_num):
        url = 'http://shenzhen.qfang.com/garden/n' + '{}'.format(page_num)
        data = requests.get(url)
        soup = BeautifulSoup(data.text,'lxml')
        houseinfo.setdefault('小区名称').append([i.text.strip() for i in soup.select('.house-title a')])   #搜寻小区名称（一页纳入列表）
        houseinfo.setdefault('小区地址',[]).append([i.select('p')[2].select('span')[0].text for i in soup.select('.show-detail')]) #搜寻小区位于的大区（一页纳入列表）
        houseinfo.setdefault('小区id',[]).append([i['href'].lstrip('/garden/desc/') for i in soup.select('.house-title a')]) #搜寻小区的链接id
        print(houseinfo)
    return houseinfo
getHouseInfo()

def getTransctionInfo():
    data_list = {}
    for i in range(1,3): #getPageNum() 对分页的列表进行循环，以获取各分页的小区概要信息
        for j in range(0,len(getHouseInfo(i)['小区id'])):  # len(getHouseInfo(i)) 小区概要信息以列表格式返回，循环进行各元素（同样为列表）的拆分
            print(getHouseInfo(i)['小区id'][j])
            url = 'http://shenzhen.qfang.com/garden/desc/'+ getHouseInfo(i)['小区id'][j] #获取二手房小区分页链接
            data = requests.get(url)
            soup = BeautifulSoup(data.text,'lxml') #获取二手房小区分页信息
#             if()
            page_num = soup.select('.turnpage_num a')[-1].text #获取二手房成交信息分页数  
            transinfo_url = 'http://shenzhen.qfang.com/garden/transactiondata/'+ getHouseInfo(i)['小区id'][j] + '/' #二手房成交链接
            transdata1 = requests.get(transinfo_url+'1') #获取第一页成交信息
            transinfo_soup1 = BeautifulSoup(transdata1.text,'lxml')
            transdata2 = requests.get(transinfo_url+ page_num) #获取最后一页成交信息
            transinfo_soup2 = BeautifulSoup(transdata2.text,'lxml')    
#             rate = int(transinfo_soup1.select('.the-fifth')[1].text.strip('元/m²'))/int(transinfo_soup2.select('.the-fifth')[-1].text.strip('元/m²'))#计算涨幅
            data_list.setdefault('小区名称',[]).append(getHouseInfo(i)['小区名称'][j])
            data_list.setdefault('小区地址',[]).append(getHouseInfo(i)['小区地址'][j])
            data_list.setdefault('建筑年代',[]).append(soup.select('.link')[0].text)
            data_list.setdefault('最近一套的面积',[]).append(transinfo_soup1.select('.the-second')[1].text)
            data_list.setdefault('最近一套的成交总价',[]).append(transinfo_soup1.select('.the-fourth')[1].text)
            data_list.setdefault('最近一套的成交时间',[]).append(transinfo_soup1.select('.the-third')[1].text)
            data_list.setdefault('最近一套的成交单价',[]).append(transinfo_soup1.select('.the-fifth')[1].text.strip('元/m²'))
            data_list.setdefault('最早一套的面积',[]).append(transinfo_soup2.select('.the-second')[-1].text)
            data_list.setdefault('最早一套的成交总价',[]).append(transinfo_soup2.select('.the-fourth')[-1].text)
            data_list.setdefault('最早一套的成交时间',[]).append(transinfo_soup2.select('.the-third')[-1].text)
            data_list.setdefault('最早一套的成交单价',[]).append(transinfo_soup2.select('.the-fifth')[-1].text.strip('元/m²'))
#             data_list.setdefault('涨幅',[]).append('{}'.format('value: %.3f' % (rate-1)))
            print(data_list)
    return data_list

def getPageNum(): #获取二手房主页面列表的分页总数
    url = 'http://shenzhen.qfang.com/garden/'
    data = requests.get(url)
    soup = BeautifulSoup(data.text,'lxml') 
    page_num = soup.select('.turnpage_num a')[-1].text.strip()
    page_num = int(page_num)
#     time.sleep(0.5)
    return page_num

df = pd.DataFrame(getTransctionInfo())
df
out = pd.ExcelWriter('D:\\output.xls')
df.to_excel(out,'Sheet1')
out.save()
