'''
@Author : Zhan Lin
@Date   : 22/9/16
'''


#  加载模块
import json
from pandas import DataFrame
import numpy as np
import openpyxl
import datetime

#  生成时间序列
def date_range(begin, end):
    dates = []
    dt = datetime.datetime.strptime(begin, "%Y-%m-%d")
    date = begin[:]
    while date < end:
        dt = dt + datetime.timedelta(1)
        dates.append(dt.strftime("%Y%m%d"))
        date = dt.strftime("%Y-%m-%d")
    print(dates[0],dates[-1],len(dates))
    return dates

#  读取json文件
def json_to_excel(file_path):
    print('Ready to write excel!')
    with open(file_path,'r',encoding='utf-8') as f:
        #  json读取
        covid_data = json.loads(f.read())

    #  产生疫情第一日到当天的昨天的
    yesterday = datetime.date.today()+ datetime.timedelta(-1)
    date_list=date_range('2020-01-18',str(yesterday))
    date_span = len(date_list)
    
    #  重塑json为二维列表
    date_province = [['dateId']]
    
    #  将标准时间序列添入列表做行键
    for dateid in date_list:
        date_province.append([dateid])

    #  实现对齐
    for p_name in covid_data:
        #  根据时间尺度大小补齐数据
        date_province[0].append(p_name)
        print('当前校正省份：',p_name)
        j = 0
        for i in range(date_span):
            try:
                dateId = str(covid_data[p_name][j]['dateId'])
            except:
                date_province[1+i].append(0)
                break
            if dateId != date_province[1+i][0]:
                date_province[1+i].append(0)
                #print('缺少日期：{}'.format(date_province[1+i][0]))
            else:
                date_province[1+i].append(covid_data[p_name][j]['confirmedIncr'])
                j += 1
    # DataFrame写入Excel
    df = DataFrame(date_province[1:],columns=date_province[0])

    df.to_csv(r'..\Visualize\China_coiv_increase.csv',encoding='utf-8',index=False)

    print('csv文件导出成功！')
   
