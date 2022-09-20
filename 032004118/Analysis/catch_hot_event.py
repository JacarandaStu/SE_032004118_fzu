'''
ddl要到了，用不了复杂的东西了
只好写个某时间片段内的某地疫情爆发检测了
'''

import numpy as np

def open_file():
    with open(r'..\Visualize\China_coiv_increase.csv','r',encoding='utf-8') as f:
        datas = []
        for line in f:
            datas.append(line.strip().split(','))
    return np.asarray(datas)

def STRANGE_POINT(data_split):

    #  统计值
    
    N = len(data_split)
    MAX = max(data_split)
    MIN = min(data_split)
    SUM = sum(data_split)
    AVR = SUM/N
    MAX_IND = MIN_IND = -1
    
    #  公式计算指标
    if (SUM-MAX)/(N-1) < 0.8*AVR:
        
        MAX_IND = np.argmax(data_split)
    if (SUM-MIN)/(N-1) > 1.2*AVR:
        if MIN != 0:
            MIN_IND = np.argmin(data_split)
    return MAX_IND,MIN_IND


if __name__ == "__main__":
    '''
    思路:截取时间片段，对各省进行遍历，
    采样这段时间内某省的最大新增数量并获取下标。
    同时计算片段内平均值，
    判断此最大值是否为具有较大影响的点。
    若删去其后平均值仅有原先80%,
    则输出最大新增数对应时间；
    疫情减缓同理。
    '''

    # 读取数据
    datas = open_file()
    
    span = (800,900)
    
    for ind in range(2,len(datas[0])):
        print('---------当前分析省份：{}----------'.format(datas[0][ind]))
        MAX_IND, MIN_IND = STRANGE_POINT(np.array(datas[span[0]:span[1],ind],
                                                  dtype='int64'))
        if MAX_IND == -1:
            print('此区间相对无爆发情况')
        else:
            print('此区间疫情爆发最严重的一天为{}'.format(datas[span[0]+MAX_IND][0]))
            print('这一天当地新增病例数为{}'.format(datas[span[0]+MAX_IND][ind]))
        if MIN_IND == -1:
            print('此区间相对无突降情况')
        else:
            if datas[span[0]+MAX_IND][0] < 0:
                print('当地存在核减政策导致有异常新增数出现')
            else:
                print('此区间突降谷底的一天为{}'.format(datas[span[0]+MAX_IND][0]))
                print('这一天当地新增病例数为{}'.format(datas[span[0]+MIN_IND][ind]))
        print()
    
    
    
