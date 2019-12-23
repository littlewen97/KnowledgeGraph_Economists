import requests
import re
import csv
import pandas as pd
from bs4 import BeautifulSoup

def download(url, num_retries=2, user_agent='wswp', proxies=None):
    '''下载一个指定的URL并返回网页内容
        参数：
            url(str): URL
        关键字参数：
            user_agent(str):用户代理（默认值：wswp）
            proxies（dict）： 代理（字典）: 键：‘http’'https'
            值：字符串（‘http(s)://IP’）
            num_retries(int):如果有5xx错误就重试（默认：2）
            #5xx服务器错误，表示服务器无法完成明显有效的请求。
            #https://zh.wikipedia.org/wiki/HTTP%E7%8A%B6%E6%80%81%E7%A0%81
    '''
    print('==========================================')
    print('Downloading:', url)
    headers = {'User-Agent': user_agent,'Connection':'close'} #头部设置，默认头部有时候会被网页反扒而出错
    try:
        resp = requests.get(url, headers=headers, proxies=proxies) #简单粗暴，.get(url)
        requests.adapters.DEFAULT_RETRIES = 6
        resp.encoding = 'utf-8'
        html = resp.text #获取网页内容，字符串形式
        if resp.status_code >= 400: #异常处理，4xx客户端错误 返回None
            print('Download error:', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                # 5类错误
                return download(url, num_retries - 1)#如果有服务器错误就重试两次

    except requests.exceptions.RequestException as e: #其他错误，正常报错
        print('Download error:', e)
        html = None
    return html #返回html

def split(basic_infos):
    '''
    处理百度百科基础信息的表格
    '''
    basic_infos = "".join(str(basic_infos).split('\n'))
    basic_infos = re.sub(r'\<dl.*?\>', "", str(basic_infos))
    basic_infos = re.sub(r'\</dl\>', "", str(basic_infos))
    basic_infos = basic_infos.split('</dd>')
    name_value = []
    for basic_info in basic_infos:
        basic_info = basic_info.split('</dt>')
        for item in basic_info:
            item = re.sub(r'\<br/\>', " ", str(item))
            #print(item)
            item = re.sub(r'\<.*?\>', "", str(item))
            if item !='':
                name_value.append(item)
    name_value = [name_value[i:i + 2] for i in range(0, len(name_value), 2)]
    #print(name_value)
    return name_value


def get_detail(html):
    soup = BeautifulSoup(html, 'html.parser')

    ch_name=en_name=abbreviation=time=category=school_type=attribute=leader=address=''
    title = soup.select('h1')[0]
    title = re.sub(r'\<.*?\>', "", str(title))

    #只爬取大学的信息
    if title.endswith('大学') or title.endswith('学院') or title.endswith('分校') or title.endswith('学校'):
        print(title)
        basic_infos = soup.select('.basicInfo-block')

        if len(basic_infos) == 2:
            # 处理基本信息表格的左边
            basicinfos_left = basic_infos[0]
            basicinfos_left = split(basicinfos_left)

            # 处理基本信息表格的右边
            basicinfos_right = basic_infos[1]
            basicinfos_right = split(basicinfos_right)

            basicinfos = basicinfos_left + basicinfos_right
            #print(basicinfos)
            for basicinfo in basicinfos:
                if len(basicinfo)==2:
                    basicinfo[0] = "".join(str(basicinfo[0]).split())
                    basicinfo[1] = re.sub(r'\[.*?\]', "", str(basicinfo[1]))
                    if basicinfo[0] == '中文名':
                        ch_name = str(basicinfo[1]).strip()
                        print("中文名：" + ch_name)
                    if basicinfo[0] == '外文名' or basicinfo[0] == '英文名':
                        en_name = str(basicinfo[1]).strip()
                        print("外文名：" + en_name)
                    if basicinfo[0] == '简称':
                        abbreviation = str(basicinfo[1]).strip()
                        print("简称：" + abbreviation)
                    if basicinfo[0] == '创办时间' or basicinfo[0] == '成立时间':
                        time = str(basicinfo[1]).strip()
                        print("创办时间：" + time)
                    if basicinfo[0] == '类别' or basicinfo[0] == '性质':
                        category = str(basicinfo[1]).strip()
                        print("类别：" + category)
                    if basicinfo[0] == '类型' or basicinfo[0] == '学校类型':
                        school_type = str(basicinfo[1]).strip()
                        print("类型：" + school_type)
                    if basicinfo[0] == '主要奖项' or basicinfo[0] == '所获称号':
                        attribute = str(basicinfo[1]).strip()
                        print("主要奖项：" + attribute)
                    if basicinfo[0] == '现任领导' or basicinfo[0] == '现任校长':
                        leader = str(basicinfo[1]).strip()
                        print("现任领导：" + leader)
                    if  basicinfo[0] == '国家' or basicinfo[0] == '所属地区' or basicinfo[0] == '所在地' or basicinfo[0] == '学校地址'or basicinfo[0] == '地址':
                        address = str(basicinfo[1]).strip()
                        print("地址：" + address)

            writer = csv.writer(open('aff_detail.csv', 'a', newline='', encoding='utf-8'))
            writer.writerow([ch_name, en_name, abbreviation, time, category, school_type, attribute, leader, address])

file_read = open('aff_url.txt',encoding='utf-8')
for line in file_read.readlines():
    html = download(str(line).strip())
    get_detail(html)

#test
#html = download("https://baike.baidu.com/item/%E7%BB%B4%E6%88%88%E5%A4%A7%E5%AD%A6/1059277")
#get_detail(html)
