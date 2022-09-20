import pandas as pd
import pandas_alive
import matplotlib.pyplot as plt

plt.style.use('ggplot')

plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False

plt.pause(0.2)

#读入数据
covid_df = pd.read_csv("China_coiv_increase.csv",
                       index_col=0,
                       parse_dates=[0])

# 绘图，动态展示最后n日数据,改变tail参数值即可修改
# 怕导出的动图太大，仅使用120天数据
covid_df.tail(120).plot_animated(
    'China_covid_view.gif',  #保存gif名称
    period_fmt="%Y/%m/%d",   #动态更新图中时间戳
    title='China Covid-19 Confirmed Increase 2020-2022',  #标题
    #perpendicular_bar_func='mean',  #添加均值辅助线
    cmap='Set1',  #定义调色盘
    n_visible=10,  #柱子显示数
    orientation='v',#柱子方向
)
