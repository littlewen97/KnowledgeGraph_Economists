import re
import bs4
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
import sys
import requests

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
    #print('==========================================')
    #print('Downloading:', url)
    headers = {'User-Agent': user_agent}  # 头部设置，默认头部有时候会被网页反扒而出错
    try:
        resp = requests.get(url, headers=headers, proxies=proxies)  # 简单粗暴，.get(url)
        html = resp.text  # 获取网页内容，字符串形式
        if resp.status_code >= 400:  # 异常处理，4xx客户端错误 返回None
            print('Download error:', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                # 5类错误
                return download(url, num_retries - 1)  # 如果有服务器错误就重试两次

    except requests.exceptions.RequestException as e:  # 其他错误，正常报错
        print('Download error:', e)
        html = None
    return html  # 返回html


#搜索百度百科并保存url，如果页面不存在则默认选择搜索的第一条链接作为url
file_read = open('aff.txt', encoding='UTF-8')
file_write = open("aff_url.txt", 'w',encoding='UTF-8')
for line in file_read.readlines():
    search_item = line.strip()
    print(search_item)
    try:
        url = 'https://baike.baidu.com/item/' + urllib.parse.quote(search_item)
        html = urllib.request.urlopen(url)
        if html.geturl() != "https://baike.baidu.com/error.html":
            file_write.write(html.geturl())
            file_write.write('\n')
            print("查看响应 url 地址：\n", html.geturl())
        else:
            url = 'https://baike.baidu.com/search/none?word=' + urllib.parse.quote(search_item)
            html = urllib.request.urlopen(url)
            # print("查找的 url 地址：\n", html.geturl())
            html = download(html.geturl().strip())
            soup = BeautifulSoup(html, 'html.parser')
            first_link = soup.select(".search-list a")
            if len(first_link) != 0:
                first_link = first_link[0]
                first_link = first_link['href'].strip()

                #确保url有http头部
                urlheader='https://baike.baidu.com'
                if urlheader in first_link:
                    file_write.write(first_link)
                    file_write.write('\n')
                    print("查看第一个 url 地址：\n", first_link)
                else:
                    first_link = 'https://baike.baidu.com' + first_link
                    file_write.write(first_link)
                    file_write.write('\n')
                    print("查看第一个 url 地址：\n", first_link)
            else:
                print("什么都没找到...")
    except AttributeError:
        print("Failed!Please enter more in details!")
file_write.close()