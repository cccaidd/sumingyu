# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:22:05 2020

@author: Administrator
"""

#导入库
import pandas as pd
import numpy as np
#导入正则表达式库
import re
import jieba

#导入数据
##header是指定哪一行为表头，None是不设置表头，默认为0
##index_col是指定那一列为索引，可以是一列也可以多列
data = pd.read_csv(r'C:\Users\Administrator\Desktop\BigData\job_info.csv',encoding='GB18030',header=None,index_col=0)
#将数据的索引设置为数据的长度
data.index = range(len(data))
#设置列名
data.columns = ['岗位名称','公司名称','工作地点','工资','发布时间','公司类型','公司规模','行业','工作描述']
#数据去重
##subset是选择多列相同的数据，inplace是是否在原数据上处理
data.drop_duplicates(subset=['岗位名称','公司名称'],inplace=True)

data.shape
'''
====================================================================================================
一、岗位名数据处理
=====================================================================================================
'''
# 1、岗位名探索
##strip是将岗位名称里面有空格或者分隔符删掉
##astype是将数据转换为str格式，lower将数据中的英文字母全部变成小写
data['岗位名称'] = data['岗位名称'].str.strip().astype(str).apply(lambda x : x.lower())
data['岗位名称'].value_counts()
#2、岗位太多太杂，我们需要筛选出待分析岗位数据
##目标岗位
target_job = ['算法','大数据','web','前端','html5','h5','开发','工程师','数据','分析','挖掘']
##用列表推导式计算岗位名称数据中哪些是属于target_job，结果为布尔值
index = [data['岗位名称'].str.count(i) for i in target_job]
##用sum按列求和index里大于0的数据，大于0表示属于目标岗位。此处得到的是布尔值
index = np.array(index).sum(axis=0) > 0
##获取想要的目标岗位
job_info = data[index]
job_info.shape

#3、将岗位名称标准化：目前岗位名称太多太杂，需要统一
job_list = ['算法','大数据','web','html5',
            'h5','前端开发','开发工程师','数据挖掘',
            '爬虫','深度学习','android','人工智能',
            'java','c++','ai','数据库','运营',
            '数据分析','软件工程']

##将job_list转换成array数组列表
job_list = np.array(job_list)

#自定义函数
##x和name_list为参数
##此处的x为岗位名称，name_list为对照列表
##index为按岗位名称去对照name_list列表，看是否属于列表中的名称
##如果是，那么index会>0，将输出该属于的名称，因属于的名称可能有多个，所有这里取第0个
##如果不是，那么index不>0，将输出原岗位名称
def rename(x=None,name_list=job_list):
    index = [i in x for i in name_list]
    if sum(index) > 0:
        return name_list[index][0]
    else:
        return x

##apply:当一个函数的参数存在于一个元组或者一个字典中时，用来间接的调用这个函数，并将元组或者字典中的参数按照顺序传递给参数
##将job_info中的岗位名称按apply的方法按照顺序传递给rename的参数x
job_info['岗位名称'] = job_info['岗位名称'].apply(rename)
##计算岗位名称中有多少不同的值和多少重复值
job_info['岗位名称'].value_counts()
'''
====================================================================================================
二、工资数据处理
目前工资是一个范围（如1.5-2.5万/月），现需取出每个岗位的最低工资与最高工资，单位为“元/月”
若招聘信息中无工资数据则无需处理。（如2-2.5万/月，则最低工资为20000，最高工资为25000。）
=====================================================================================================
'''
##查看工资最后一个字的重复值有多少
job_info['工资'].str[-1].value_counts()
##查看工资倒数第三个字的重复值有多少
job_info['工资'].str[-3].value_counts()
##提取工资的最后一个字去传递给lambda看是否属于月或年，返回的是布尔值
index1 = job_info['工资'].str[-1].apply(lambda x: x in ['月','年'])
##提取工资的倒数第三个字去传递给lambda看是否属于万或千，返回的是布尔值
index2 = job_info['工资'].str[-3].apply(lambda x: x in ['万','千'])
##工资列提取即属于index1同时也属于index2的数据，把不属于的值去除掉
job_info = job_info[index1 & index2]


#自定义函数
##x为参数，这里的i为数据中的工资数
##如果x的倒数第三个字为万，那么从x提取出工资数i，再把i变成浮点数×10000
##否则如果x的倒数第三个字为千，那么从x提取出工资数i，再把i变成浮点数×1000
##如果x的最后一个字为年，那么i除以12求出每个月的工资。这里的i是在运行了上面的基础上所以for i in a
##最后输出最终的工资
##如果不符合try里面的语句，那么输出原数据x
def get_max_min(x=None):
    try:
        if x[-3] == '万':
            a = [float(i)*10000 for i in re.findall('\d+\.?\d*',x)]
        elif x[-3] == '千':
            a = [float(i)*1000 for i in re.findall('\d+\.?\d*',x)]
        if x[-1] == '年':
            a = [i/12 for i in a]
        return a
    except:
        return x

##将job_info中的工资按apply的方法按照顺序传递给get_max_min的参数x
salary = job_info['工资'].apply(get_max_min)

##提取最低工资，取salary里的第0个数据
job_info['最低工资'] = salary.str[0]
##提取最高工资，取salary里的第1个数据
job_info['最高工资'] = salary.str[1]
##计算工资水平，用最低工资和最高工资求均值，axis=1是按行计算
job_info['工资水平'] = job_info[['最低工资','最高工资']].mean(axis=1)

'''
====================================================================================================
三、工作地点处理
=====================================================================================================
'''

# 1、工作地点统一命名
xia1 = job_info['工作地点'].value_counts()
address_list = ['广州', '深圳', '上海', '北京', '武汉', '成都', '杭州',
                '佛山', '苏州', '珠海', '东莞', '南京', '长沙', '厦门',
                '中山', '西安', '重庆', '无锡', '合肥', '福州', '常州',
                '郑州', '江门', '宁波', '济南', '石家庄', '嘉兴', '贵阳',
                '昆明', '南通','温州']
address_list = np.array(address_list)

def rename(x=None,name_list=address_list):
    index = [i in x for i in name_list]
    if sum(index) > 0:
        return name_list[index][0]
    else:
        return x

job_info['工作地点'] = job_info['工作地点'].apply(rename)

'''
====================================================================================================
四、公司类型数据处理
=====================================================================================================
'''
##查看数据，发现数据中含有[],['']等无用数据
job_info['公司类型'].value_counts()
#对无用数据做处理
#loc函数主要通过行标签索引行数据，划重点，标签！标签！标签！
#iloc 主要是通过行号获取行数据，划重点，序号！序号！序号！
##用loc标签索引公司类型，用apply方法把公司类型传递到lambda语句里，得出如果x的长度<6，就把它变成nan
job_info.loc[job_info['公司类型'].apply(lambda x: len(x) < 6),'公司类型'] = np.nan
##因为公司类型是str类型数据，所以提取时直接str就好。
##这里提取公司类型的[2:-2]刚好是整个公司类型
job_info['公司类型'] = job_info['公司类型'].str[2:-2]
##最后查看预处理完的公司类型，已经没有[],['']了
job_info['公司类型'].value_counts()


'''
====================================================================================================
五、行业数据处理
=====================================================================================================
'''
##查看数据，发现数据中含有[]等无用数据
job_info['行业'].value_counts()
#对无用数据做处理
##用loc标签索引行业，用apply方法把行业传递到lambda语句里，得出如果x的长度<6，就把它变成nan
job_info.loc[job_info['行业'].apply(lambda x: len(x) < 6),'行业'] = np.nan
##因为行业的数据类型不是str所以无法直接提取，且行业类型有多种，这里只取第一种。
##split() 是通过指定分隔符对字符串进行切片
##先把整个行业提取出来，因有多种行业用分隔符把它分开，再提取第一种行业
job_info['行业'] = job_info['行业'].str[2:-2].str.split(',').str[0]
##最后查看预处理完的公司类型，已经没有那么多行业了
job_info['行业'].value_counts()

'''
====================================================================================================
六、工作描述数据处理
=====================================================================================================
'''
##读取停用词数据，'r'为只读
with open(r'C:\Users\Administrator\Desktop\BigData\stopword.txt','r') as f :
    stopword = f.read()
##
a = job_info['工作描述'].str[2:-2].apply(lambda x: x.lower()).apply(lambda x: ''.join(x)).apply(jieba.lcut).apply(lambda x: [i for i in x if i not in stopword])
a[a.apply(lambda x: len(x) < 6)] = np.nan
job_info['工作描述'] = a


'''
====================================================================================================
七、公司人数进行处理
=====================================================================================================
'''
##查看公司规模数据的情况
job_info['公司规模']
#自定义函数
##x为参数，负责传入数据。i为公司规模的人数数据
##尝试将数据传入x，让i用findall去提取x中的数字，再转为int整型数据赋给a
##如果a的长度等于1，那么把a的第0个数据赋给n，最后输出n
##如果a的长度等于2，那么计算a的均值后赋给n，最后输出n
##如果因数据为空无法提取，则将数据转换为nan
def get_number_staff(x=None):
    try:
        a = [int(i) for i in re.findall('\d+',x)]
        if len(a) == 1:
            n = a[0]
        elif len(a) == 2:
            n = np.mean(a)
        return n
    except:
        return np.nan
##将公司规模传送到上面的自定义函数
job_info['公司规模'] = job_info['公司规模'].apply(get_number_staff)

'''
===============
八、构造新数据
===============
'''
##查看数据的所有列名
job_info.columns
##创建清洗后新数据中需要的列名
features = ['岗位名称','公司名称','工作地点','工资水平','公司规模','发布时间','公司类型','行业','工作描述']
##按features去提取旧数据作为新数据
data_new = job_info[features]
data_new.to_csv('C:/Users/Administrator/Desktop/BigData/job_info_new.csv',encoding='GB18030',index=None)





