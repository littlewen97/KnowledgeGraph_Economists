from bs4 import BeautifulSoup
import requests
import re
import csv
class Spider():
    def getSoup(self,url):
        kv = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
        r = requests.get(url,headers=kv,allow_redirects=False)
        r.encoding = r.apparent_encoding
        response = r.text
        soup = BeautifulSoup(response,'html.parser')
        return soup

    def getContent(self,soup):
        # a b 分别为百度百科前两段内容
        paras = soup.find_all('div',class_='para')
        para1 = str(paras[0].get_text()) if paras[0] else ''
        para2 = str(paras[1].get_text()) if paras[1] else ''
        a = re.sub('\[\d?-?\d\]|[\r\t\n\xa0]','',para1)
        b = re.sub('\[\d?-?\d\]|[\r\t\n\xa0]','',para2)
        # 以下分别为全名、国籍、职业、代表作、成就
        items_name = soup.find_all('dt',class_='basicInfo-item name')
        items_value = soup.find_all('dd',class_='basicInfo-item value')
        items = dict()
        items['第一段'] = a
        items['第二段'] = b
        for name,value in zip(items_name,items_value):
            temp1 = re.sub('\[\d?-?\d\]|[\r\t\n\xa0]','',name.get_text())
            temp2 = re.sub('\[\d?-?\d\]|[\r\t\n\xa0]','',value.get_text())
            items[temp1] = temp2
        return items

    def printContent(self,items):
        for item in items:
            print(item + ": " + items[item])
    def createPersonCSV(self,items):
        path = 'Person.csv'
        Chinese_Full_Name = items['中文名'] if ('中文名' in items.keys()) else items['本名']
        with open(path,'a+',newline='',encoding='utf-8') as f:
            csv_write = csv.writer(f)
            English_Full_Name = items['外文名'] if('外文名' in items.keys()) else ''
            Occupation = items['职业'] if('职业' in items.keys()) else ''
            Achievements = items['主要成就'] if ('主要成就' in items.keys()) else ''
            csv_write.writerow([Chinese_Full_Name,English_Full_Name,Occupation,Achievements])
    def createCountryCSV(self,items):
        path = 'Country.csv'
        nationality = items['国籍'] if('国籍' in items.keys()) else items['出生地']
        if (nationality == ''):
            return
        #读取第一列，查询是否有重复
        with open(path, 'rb') as f:
            reader = csv.reader(f)
            column = [row[0] for row in reader]
            if (nationality in column):
                return
        data = ''
        rank = ''
        policy = ''
        with open(path, 'a+', newline='') as f:
            csv_write = csv.writer(f)
            csv_write.writerow([nationality,data,rank,policy])
    def createMasterpiece(self,items):
        path = 'Masterpiece.csv'
        masterpiece = ''
        if('代表作品' in items.keys()):
            masterpiece = items['代表作品']
        if(masterpiece==''):
            return
        with open(path,'rb') as f:
            reader = csv.reader(f)
            column = [row[0] for row in reader]
            if(masterpiece in column):
                return
        with open(path,'a+',newline='') as f:
            csv_write = csv.writer(f)
            csv_write.writerow([masterpiece])
    def createSchool(self,items):
        path = "School.csv"
