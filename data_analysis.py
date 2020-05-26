# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:44:15 2020

@author: Administrator
"""


import pandas as pd
import matplotlib.pyplot as plt

job_info_new = pd.read_csv(r'C:/Users/Administrator/Desktop/BigData/job_info_new.csv',encoding='GB18030')


# 热门岗位
gw = job_info_new['岗位名称'].value_counts()[:10]
plt.figure(figsize=(16,9))
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.subplots_adjust(bottom=0.15)
plt.bar(gw.index,gw,width=0.5)
plt.xticks(rotation=35)
plt.title('热门招聘岗位')
plt.savefig(r'C:/Users/Administrator/Desktop/BigData/img/热门招聘岗位.png')
plt.show()


# 热门行业
hy = job_info_new['行业'].value_counts()[:10]
plt.figure(figsize=(16,9))
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.subplots_adjust(bottom=0.25)
plt.bar(hy.index,hy,width=0.5)
plt.xticks(rotation=35)
plt.title('热门行业分布')
plt.savefig(r'C:/Users/Administrator/Desktop/BigData/img/热门行业分布.png')
plt.show()


# 热门招聘公司分布
gs = job_info_new['公司名称'].value_counts()[:10]
plt.figure(figsize=(16,9))
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.subplots_adjust(bottom=0.15)
plt.bar(gs.index,gs,width=0.5)
plt.xticks(rotation=35)
plt.title('热门招聘公司分布')
plt.savefig(r'C:/Users/Administrator/Desktop/BigData/img/热门招聘公司分布.png')
plt.show()


# 热门岗位的薪资待遇
##把数据按groupby拆分数据再用agg聚合数据
##按岗位名称去拆分然后提取工资水平列和公司名称列，分别计算均值和总数。
##用sort_values方法按公司名称排升降序，False是从大到小
gw_xz1 = job_info_new.groupby('岗位名称').agg({'工资水平':'mean','公司名称':'count'}).sort_values('公司名称',ascending=False)
gw_xz2 = gw_xz1['工资水平'][:10]
plt.figure(figsize=(16,9))
##设置中文字体
plt.rcParams['font.sans-serif'] = 'SimHei'
##设置图片的下边框
plt.subplots_adjust(bottom=0.15)
##画状形图  width为设置状体的宽度
plt.bar(gw_xz2.index,gw_xz2,width=0.5)
##头部名
plt.title('热门岗位的薪资待遇')
##保存图片
plt.savefig(r'C:/Users/Administrator/Desktop/BigData/img/热门岗位的薪资待遇.png')
plt.show()


# 热门行业的薪资待遇
##把数据按groupby拆分数据再用agg聚合数据
##按行业去拆分然后提取工资水平列和公司名称列，分别计算均值和总数。
##用sort_values方法按公司名称排升降序，False是从大到小
hy_xz1 = job_info_new.groupby('行业').agg({'工资水平':'mean','公司名称':'count'}).sort_values('公司名称',ascending=False)
hy_xz2 = hy_xz1['工资水平'][:10]
plt.figure(figsize=(16,9))
##设置中文字体
plt.rcParams['font.sans-serif'] = 'SimHei'
##设置图片的下边框
plt.subplots_adjust(bottom=0.25)
##画状形图  width为设置状体的宽度
plt.bar(hy_xz2.index,hy_xz2,width=0.5)
##设置底下倾斜度
plt.xticks(rotation=35)
##头部名
plt.title('热门行业的薪资待遇')
##保存图片
plt.savefig(r'C:/Users/Administrator/Desktop/BigData/img/热门行业的薪资待遇.png')
plt.show()


# 热门城市的工资水平
##把数据按groupby拆分数据再用agg聚合数据
##按工作地点去拆分然后提取工资水平列和公司名称列，分别计算均值和总数。
##用sort_values方法按公司名称排升降序，False是从大到小
city_xz1 = job_info_new.groupby('工作地点').agg({'工资水平':'mean','公司名称':'count'}).sort_values('公司名称',ascending=False)
city_xz2 = city_xz1['工资水平'][:10]
plt.figure(figsize=(16,9))
##设置中文字体
plt.rcParams['font.sans-serif'] = 'SimHei'
##设置图片的下边框
plt.subplots_adjust(bottom=0.15)
##画状形图  width为设置状体的宽度
plt.bar(city_xz2.index,city_xz2,width=0.5)
##设置底下倾斜度
plt.xticks(rotation=35)
##头部名
plt.title('热门城市的工资水平')
##保存图片
plt.savefig(r'C:/Users/Administrator/Desktop/BigData/img/热门城市的工资水平.png')
plt.show()

# 热门城市的招聘分布
city = job_info_new['工作地点'].value_counts()[:10]
plt.figure(figsize=(16,9))
##设置中文字体
plt.rcParams['font.sans-serif'] = 'SimHei'
##设置图片的下边框
plt.subplots_adjust(bottom=0.15)
##画状形图  width为设置状体的宽度
plt.bar(city.index,city,width=0.5)
##设置底下倾斜度
plt.xticks(rotation=35)
##头部名
plt.title('热门城市的招聘分布')
##保存图片
plt.savefig(r'C:/Users/Administrator/Desktop/BigData/img/热门城市的招聘分布.png')
plt.show()


# 不同体量企业的薪资待遇
##因为公司规模不超过10个，所以不用取前10个。
##这里主要有公司规模和薪资待遇就好，所以只用到公司规模和工资水平
gm_xz1 = job_info_new.groupby('公司规模').agg({'工资水平':'mean'})
plt.figure(figsize=(16,9))
##设置中文字体
plt.rcParams['font.sans-serif'] = 'SimHei'
##设置图片的下边框
plt.subplots_adjust(bottom=0.15)
##画状形图  width为设置状体的宽度
##因为gm_xz1的类型是数据框，所以不能像上面那样用。
##只能取它的长度做x轴，所需的列名为y轴
plt.bar(range(len(gm_xz1)),gm_xz1['工资水平'],width=0.5)
##头部名
plt.title('不同体量企业的工资水平')
##rotation设置底下倾斜度
##要取数据框数据对应的x轴名称要先取长度，再取index列
plt.xticks(range(len(gm_xz1)),gm_xz1.index,rotation=35)
##保存图片
plt.savefig(r'C:/Users/Administrator/Desktop/BigData/img/不同体量企业的工资水平.png')
plt.show()


# 不同体量公司的用人需求
##按照需求，这里要做的是按照公司规模去提取公司名称出现的次数，从而得出用人需求量
gm_xq = job_info_new.groupby('公司规模').agg({'公司名称':'count'})
plt.figure(figsize=(16,9))
##设置中文字体
plt.rcParams['font.sans-serif'] = 'SimHei'
##设置图片的下边框
plt.subplots_adjust(bottom=0.15)
##画状形图  width为设置状体的宽度
##因为gm_xq的类型是数据框，所以不能像上面那样用。
##只能取它的长度做x轴，所需的列名为y轴
plt.bar(range(len(gm_xq)),gm_xq['公司名称'],width=0.5)
##rotation设置底下倾斜度
##要取数据框数据对应的x轴名称要先取长度，再取index列
plt.xticks(range(len(gm_xq)),gm_xq.index,rotation=45)
##头部名
plt.title('不同体量公司的用人需求')
##保存图片
plt.savefig(r'C:/Users/Administrator/Desktop/BigData/img/不同体量公司的用人需求.png')
plt.show()


# 岗位技能分析





