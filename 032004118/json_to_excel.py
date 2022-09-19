'''
@Author : Zhan Lin
@Date   : 22/9/16
'''


#  加载模块
import json
from pandas import DataFrame
import numpy as np
import openpyxl

def json_to_excel(file_path):
    print('Ready to write excel!')
    with open(file_path,'r',encoding='utf-8') as f:
        
        #  json读取
        covid_data = json.loads(f.read())

    ##  找到最大天数以实现天数为键对齐值

    date_province = [['dateId']]
    Max_date = 0
    max_key = None
    #  提取最大天数信息以及属性标签
    for key in covid_data:
        date_province[0].append(key)
        span = len(covid_data[key])
        if Max_date < span:
            Max_date = span
            max_key = key

    #  写入时间Id
    for i in range(Max_date):
        date_province.append([covid_data[max_key][i]['dateId']])

    #  实现对齐
    for p_name in date_province[0][1:]:
        #  根据时间尺度大小补齐数据
        date_span = len(covid_data[p_name])
        
        if date_span < Max_date:
            for k in range(Max_date-date_span):
                date_province[k+1].append(0)
        for i in range(date_span):
            date_province[Max_date-date_span+1+i].append(covid_data[p_name][i]['confirmedIncr'])

    # DataFrame写入Excel
    df = DataFrame(date_province[1:],columns=date_province[0])

    df.to_excel('China_coiv_increase.xlsx',encoding='utf-8',index=False)

   
