# coding: utf-8

import requests
from bs4 import BeautifulSoup 
import pandas as pd
import csv
import time

def getHouseInfo():   #获取各小区的概要信息（小区名称、地址、ID等）
    housename =[]
#     location = []
    househref = []
    houseID = []
    page_num=getPageNum() #获取主页面列表的分页数
    for i in range(1,2):
        url = 'https://sz.lianjia.com/ershoufang/pg' + '{}'.format(i)
        data = requests.get(url)
        soup = BeautifulSoup(data.text,'lxml')
        housename.extend([i.text.strip() for i in soup.select('.houseInfo a')])   #搜寻小区名称（一页纳入列表）
#         location.extend([i.select('p')[2].select('span')[0].text for i in soup.select('.show-detail')]) #搜寻小区位于的位置
        househref.extend([i['href'] for i in soup.select('.houseInfo a')]) #搜寻小区的链接
#         houseID.extend([i['data-housecode'] for i in soup.select('.title a')]) #搜寻小区的链接
        print(housename)
        print(househref)
        print(houseID)
    return housename,househref
getHouseInfo()

def getPageNum(): #获取二手房主页面列表的分页总数
    url = 'https://sz.lianjia.com/ershoufang/'
    data = requests.get(url)
    soup = BeautifulSoup(data.text,'lxml') 
    page_num = soup.select('.page-box.house-lst-page-box')[0]['page-data']
    page_num = eval(page_num)['totalPage']
    bb = []
    for i in soup.select('.title a'):
        print(''.join(i['data-housecode']) 
#     time.sleep(0.5)
    return page_num
getPageNum()
