import requests
import re
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
    headers = {'User-Agent': user_agent} #头部设置，默认头部有时候会被网页反扒而出错
    try:
        resp = requests.get(url, headers=headers, proxies=proxies) #简单粗暴，.get(url)
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


# #获取经济学家的详情页面的url（前5%）
# def get_shorttop(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     file_write = open("ideas_url.txt", 'w', encoding='UTF-8')
#     #获取经济学家对应的url
#     ideas_url = []
#     names = soup.select('.shorttop td:nth-child(2)>a:nth-child(1)')
#     for item in names:
#         #print("https://ideas.repec.org/"+item['href'])
#         file_write.write("https://ideas.repec.org"+item['href'])
#         file_write.write('\n')
#     print("shorttop url success!")
#
# #获取经济学家详情页面的url（6%到10%）
# def get_top6to10(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     names = soup.select('#ranking>a')
#
#     with open("ideas_url.txt", "a") as file_write:
#         for item in names:
#             file_write.write("https://ideas.repec.org"+item['href'])
#             file_write.write('\n')
#     print("top6to1 url success!")

def get_all(path,html):
    soup = BeautifulSoup(html, 'html.parser')
    url= soup.select(path)
    get_url(url,"ideas_url_all.txt")
    print(path+' finished')

def get_url(url,file):
    with open(file, "a") as file_write:
        for item in url:
            file_write.write("https://ideas.repec.org" + item['href'])
            file_write.write('\n')


html = download('https://ideas.repec.org/i/eall.html')
for i in range(5,56,2):
    path="table:nth-child("+ str(i) +")>tr>td>a"
    get_all(path,html)
