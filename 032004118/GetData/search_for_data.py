'''
@Author : Zhan Lin
@Date   : 22/9/16
'''


#  加载模块
import time
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

from json_to_excel import json_to_excel as j2e

headers={

        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33'

        }

#  请求地址

url='https://ncov.dxy.cn/ncovh5/view/pneumonia?from=timeline&isappinstalled=0'

requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接

def get_info(data):
    new_confirmed_history = []
    for dic in data:
        one_day = {}
        one_day['confirmedIncr'] = dic['confirmedIncr']
        one_day['dateId'] = dic['dateId']
        new_confirmed_history.append(one_day)
    return new_confirmed_history

#  解析字段
response = requests.get(url,headers = headers, timeout = 300)
response.encoding = 'utf-8'
content = response.content.decode('utf-8')
soup = BeautifulSoup(response.text,'lxml')

## Web Search Model
print('**ready to search**')

start = time.time()
#  爬取网页文档中对应记录我国疫情情况的部分
data = soup.find_all(name = 'script',attrs = {'id':'getAreaStat'})
#  爬取以国名为provinceNmae的json文件
Sum_data = soup.find_all(name = 'script',attrs = {'id':'getListByCountryTypeService2true'})
#  获取其中存储数据的json格式部分
#  这里是发现其存储在一对try..catch之中
account = str(data)
account1 = str(Sum_data)
#  转换json文件
l = account.find('[',2)     #匹配第二个[
r = account.rfind(']',0,-2) #匹配倒二个]
covid = account[l:r+1]      #对应切片内容即为json格式数据
covid_json = json.loads(covid)

l = account1.find('[',2)     #匹配第二个[
r = account1.rfind(']',0,-2) #匹配倒二个]
covid = account1[l:r+1]      #对应切片内容即为json格式数据
world_covid_json = json.loads(covid)

#  一级json文件取得
end = time.time()
print('一级json文件取得,耗时{:.6f}s'.format(end-start))

#  json文件操作
#  中国大陆独立操作

area = {}

#  历史疫情数据爬取
start = time.time()

China = world_covid_json[10]
assert China['provinceName'] == '中国'
response = requests.get(China['statisticsData'],
                        headers = headers,
                        timeout = 300)
response.encoding = 'utf-8'
content = response.content.decode('utf-8')
his_json = json.loads(content)
data = his_json['data']
area[China['provinceName']] = get_info(data)

end = time.time()
print('中国大陆历史疫情数据载入完毕！\n耗时{:.6f}s'.format(end-start))


for province in covid_json:
    start = time.time()
    #  获取statisticsData键对应存放的json文件数据
    if 'statisticsData' in province:
        response = requests.get(province['statisticsData'],
                                headers = headers,
                                timeout = 300)
        response.encoding = 'utf-8'
        content = response.content.decode('utf-8')
        his_json = json.loads(content)
        data = his_json['data']
        area[province['provinceName']] = get_info(data)

    #  记时
    end = time.time()
    print('{} 历史疫情数据爬取完毕!耗时{:.6f}s'.format(province['provinceName'],
                                           end-start))
    
file_path = 'China_covid_history.json'
with open(file_path,'w',encoding='utf-8') as f:
    json.dump(area, f)

j2e(file_path)


