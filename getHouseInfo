import requests
from bs4 import BeautifulSoup 
def getHouseInfo():
    url = 'http://shenzhen.qfang.com/garden/desc/58039'
    data = requests.get(url)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text,'lxml')
    house_name = soup.find_all('h2')[0].text
    location = soup.select('.garden-address')[0].text
    return house_name,location
getHouseInfo()

#def getTradeInfo(url): #获取历史成交记录数据
url = 'http://shenzhen.qfang.com/garden/transactiondata/58039/1'
res = requests.get(url)
print(res)
soup = BeautifulSoup(res.text,'lxml')
soup

data_list = {}
data_list['小区名称'] = ['{}'.format(getHouseInfo()[0])]
data_list['面积'] = [soup.select('.the-second')[1].text]
data_list['最近一套的成交总价'] = [soup.select('.the-fourth')[1].text]
data_list['成交时间'] = [soup.select('.the-third')[1].text]
data_list['成交单价'] = [soup.select('.the-fifth')[1].text.strip('元/m²')]


import pandas as pd
df = pd.DataFrame(data_list)
df
