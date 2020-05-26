# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:25:34 2020

@author: Administrator
"""


import requests
import pandas as pd
from lxml import etree
import time

#网页
##HTML5开发工程师
url_tou = 'https://search.51job.com/list/000000,000000,0000,00,9,99,HTML5%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,'
url_wei = '.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

for i in range(1,22):
    print('正在爬取第', i,'页招聘数据')
    url = url_tou + str(i) + url_wei
    #伪造User-Agent
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    #调用requests.get去获取网页
    web = requests.get(url,headers=headers)
    #输出源码数据
    #print(web.text)   #打印出的数据有乱码现象，需转为中文
    web.encoding = 'GBK'   #转为中文
    #print(web.text)   #转换后输出正常
    #dom是网页结构数
    dom = etree.HTML(web.text)  #用etree.HTML进行网页数据解析web.text赋给dom
    ##获取岗位名称
    #用dom结构数提取信息
    job_name = dom.xpath('//div[@class="dw_table"]/div[@class="el"]//p/span/a[@target="_blank"]/@title')
    ##获取公司名称
    company_name = dom.xpath('//div[@class="dw_table"]/div[@class="el"]//span[@class="t2"]/a[@target="_blank"]/@title')
    ##获取工作地点
    address = dom.xpath('//div[@class="dw_table"]/div[@class="el"]//span[@class="t3"]/text()')
    ##获取薪资信息
    salary_mid = dom.xpath('//div[@class="dw_table"]/div[@class="el"]//span[@class="t4"]')
    #因部分招聘信息的薪资未公布，故需要做进一步处理
    salary = [i.text for i in salary_mid]
    ##获取发布时间信息
    date = dom.xpath('//div[@class="dw_table"]/div[@class="el"]//span[@class="t5"]/text()')
    
    ##新建空列表，用于后面存放数据
    JobIofo = []
    CompanyIofo = []
    NumberStaff = []
    Industry = []
    ##获取二级网页网址
    href = dom.xpath('//div[@class="dw_table"]/div[@class="el"]//p/span/a[@target="_blank"]/@href')
    ##用for循环获取所有二级网页信息
    for i in range(len(href)):
        web_sub = requests.get(href[i])  #获取网址信息 
        web_sub.encoding = 'GBK'  #转为中文
        dom_sub = etree.HTML(web_sub.text)
          #获取二级网页职位信息
        job_info = dom_sub.xpath('//div[@class="tCompany_main"]//div[@class="bmsg job_msg inbox"]/p/text()')
          #获取二级网页公司类型
        company_info = dom_sub.xpath('//div[@class="tBorderTop_box"]/div[@class="com_tag"]/p[1]/@title')
          #获取二级网页公司员工人数信息
        number_staff = dom_sub.xpath('//div[@class="tBorderTop_box"]/div[@class="com_tag"]/p[2]/@title')
          #获取二级网页公司行业信息
        industry = dom_sub.xpath('//div[@class="tBorderTop_box"]/div[@class="com_tag"]/p[3]/@title')
        
        JobIofo.append(job_info)
        CompanyIofo.append(company_info)
        NumberStaff.append(number_staff)
        Industry.append(industry)
        
        time.sleep(2)
    
    da = pd.DataFrame()
    da['岗位名称'] = job_name
    da['公司名称'] = company_name
    da['工作地点'] = address
    da['工资'] = salary
    da['发布时间'] = date
    da['公司类型'] = CompanyIofo
    da['公司人数'] = NumberStaff
    da['行业'] = Industry
    da['工作描述'] = JobIofo
    #数据写入保存
    ##此处无法用GBK和GB2312编码，用的GB18030是GBK的父集
    da.to_csv('C:/Users/Administrator/Desktop/BigData/job_info.csv',mode='a+',header=None,encoding='GB18030')
    time.sleep(3)

