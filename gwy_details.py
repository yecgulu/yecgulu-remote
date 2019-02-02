# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 10:58:04 2019

@author: Han
"""

import requests
import re
import bs4
#import os
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq


list1 = []
list_address = []
num = 0
stop = 0
#def 抓网页
def getHTML(url):
    try:
        r = requests.get(url, timeout = 5)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return  ""


#def 分析网页内容
def fillPARSER(list1, html):
   
    soup = BeautifulSoup(html, 'html.parser')
    trALL = soup.find_all('tr')  
    
    for tr in trALL:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            try:
                if eval(tds[6].string) > 200:
                    list1.append([tds[0].string, tds[1].string, tds[2].string, tds[3].string, tds[5].string, tds[6].string,tds[7].a['href']])
                    global num 
                    num = num + 1
                    print(num)
                else:
                    global stop 
                    stop = 1
                    break
            except IndexError:
                pass

#def 分析细节网页内容
def fillPquery(list1,html,index):

    doc = pq(html)
    for i in doc('div.gkzwfl ul li span.zwxxbt'):
        if i.text=='学历':
            index_xl =doc('div.gkzwfl ul li span.zwxxbt').index(i)
            xl = doc('div.gkzwfl ul li span.zwxxbt').siblings()[index_xl].text
            list1[index].append(xl)
        if i.text=='专业':
            index_zy =doc('div.gkzwfl ul li span.zwxxbt').index(i)
            zy = doc('div.gkzwfl ul li span.zwxxbt').siblings()[index_zy].text
            list1[index].append(zy)
        print(list1[index][7])
        print(list1[index][8])


#def 输出到文件
def printLIST(list1, num):
    output = open("list2.txt", "w+")
    for i in range(num):
        ls=list1[i]
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\r\n".format(ls[0],ls[1],ls[2],ls[3],ls[4],ls[5],ls[7],ls[8]),file =output)
    output.close

    output1 = open("pos2.txt", "w+")
    for i in range(num):
        ls=list1[i]
        print("{}\r\n".format(ls[1]),file =output1)
    output1.close
    
    output1 = open("学历.txt", "w+")
    for i in range(num):
        ls=list1[i]
        print("{}\t{}\r\n".format(ls[1],ls[7]),file =output1)
    output1.close
    
    output1 = open("专业.txt", "w+")
    for i in range(num):
        ls=list1[i]
        print("{}\t{}\r\n".format(ls[1],ls[8]),file =output1)
    output1.close
    
def main():
    
    for page in range(483):
        page1 = page + 1
        url = "http://ah.huatu.com/zw/rank/?act=jzb&page="+str(page1)
        if stop != 1:
            html = getHTML(url)
            fillPARSER(list1, html)
            print(page1)
            print(num)
        else:
            break
    
    for i in list1:
        i[6]=re.sub(r'\.\.\/2019','http://ah.huatu.com/zw/2019',i[6])
        print(i[6])
        list_address.append(i[6])
                
    for i in list_address:
        print(i)
        index = list_address.index(i)
        print(index)
        htmlDetail=getHTML(i)
        fillPquery(list1,htmlDetail,index)
            
    printLIST(list1,num)
       
        
main()        