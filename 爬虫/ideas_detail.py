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
        resp = requests.get(url, headers=headers, proxies=proxies)
        requests.adapters.DEFAULT_RETRIES = 6
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


def get_works(html):
    soup = BeautifulSoup(html, 'html.parser')

    #获取经济学家姓名
    name = soup.select('title')
    name = re.sub(r'\<.*?\>', "", str(name))
    name = ((str(name).split('|'))[0].strip())[1:]
    #print("姓名：" + name)

    #获取经济学家所属组织
    affiliations = soup.select("#affiliation > h3")
    #print(len(affiliations))
    aff_list = []
    affiliation1 = affiliation2 = ''
    # print(type(affiliations))
    for item in affiliations:
        aff_text=str(item).split('<br/>')[-1]
        aff_text = re.sub(r'\(.*?%\)', "", str(aff_text))
        aff_text = re.sub(r'\<.*?\>', "", aff_text)
        aff_list.append(aff_text.strip())
        # print(aff_text.strip())

    if len(aff_list) == 0:
        affiliation1 = ''
        affiliation2 = ''
    elif len(aff_list) == 1:
        affiliation1 = aff_list[0]
        affiliation2 = ''
    else:
        affiliation1 = aff_list[0].strip('\t')
        affiliation2 = aff_list[1].strip('\t')
    #print("所属部门1：" + affiliation1)
    #print("所属部门2：" + affiliation2)

    #获取经济学家发表的文章（最多10个）
    work_list = []
    works = soup.select('#research > ol')
    works = works[0].select('.publishedas>ul>li>b')
    for item in works:
        item = re.sub(r'\<.*?\>', "", str(item))
        work_list.append(item)

    published=['']*10
    if len(work_list) >= 10:
        for i in range(10):
            published[i] = work_list[i]
    if len(work_list) < 10:
        for i in range(len(work_list)):
            published[i] =work_list[i]

    #写入economists_all.csv文件
    writer=csv.writer(open('economists_all.csv', 'a', newline='', encoding='utf-8'))
    writer.writerow([name, affiliation1, affiliation2, published[0], published[1], published[2],
                       published[3], published[4], published[5], published[6], published[7],
                          published[8], published[9]])



file_read = open('ideals_url_all.txt',encoding='utf-8')
for line in file_read.readlines():
    html = download(str(line).strip())
    get_works(html)
